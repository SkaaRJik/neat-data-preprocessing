import json
import logging.config
import traceback
from random import random

import matplotlib.pyplot as plt
import networkx as nx
import yaml
from pyvis.network import Network
from networkx.drawing.nx_pydot import graphviz_layout

from src.config.RabbitMQConfig import RabbitMQConfig
from src.config.SambaConfig import SambaConfig
from src.rabbitmq.RabbitMQWorker import RabbitMQWorker
from src.rabbitmq.consumer.NormalizationDataConsumer import NormalizationDataConsumer
from src.rabbitmq.consumer.ReportResultConsumer import ReportResultConsumer
from src.rabbitmq.consumer.VerifyDocuementConsumer import VerifyDocumentConsumer
from src.samba.SambaWorker import SambaWorker

logging.config.fileConfig('../resources/logging.conf')
LOGGER = logging.getLogger("infoLogger")

with open('../resources/application-dev.yml') as f:
    global_config = yaml.safe_load(f)

rabbitMqConfig: RabbitMQConfig = RabbitMQConfig(global_config)
sambaConfig: SambaConfig = SambaConfig(global_config)





def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, leaf_vs_root_factor=0.5):
    '''
    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    Based on Joel's answer at https://stackoverflow.com/a/29597209/2966723,
    but with some modifications.

    We include this because it may be useful for plotting transmission trees,
    and there is currently no networkx equivalent (though it may be coming soon).

    There are two basic approaches we think of to allocate the horizontal
    location of a node.

    - Top down: we allocate horizontal space to a node.  Then its ``k``
      descendants split up that horizontal space equally.  This tends to result
      in overlapping nodes when some have many descendants.
    - Bottom up: we allocate horizontal space to each leaf node.  A node at a
      higher level gets the entire space allocated to its descendant leaves.
      Based on this, leaf nodes at higher levels get the same space as leaf
      nodes very deep in the tree.

    We use use both of these approaches simultaneously with ``leaf_vs_root_factor``
    determining how much of the horizontal space is based on the bottom up
    or top down approaches.  ``0`` gives pure bottom up, while 1 gives pure top
    down.


    :Arguments:

    **G** the graph (must be a tree)

    **root** the root node of the tree
    - if the tree is directed and this is not given, the root will be found and used
    - if the tree is directed and this is given, then the positions will be
      just for the descendants of this node.
    - if the tree is undirected and not given, then a random choice will be used.

    **width** horizontal space allocated for this branch - avoids overlap with other branches

    **vert_gap** gap between levels of hierarchy

    **vert_loc** vertical location of root

    **leaf_vs_root_factor**

    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  # allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, leftmost, width, leafdx=0.2, vert_gap=0.2, vert_loc=0,
                       xcenter=0.5, rootpos=None,
                       leafpos=None, parent=None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''

        if rootpos is None:
            rootpos = {root: (xcenter, vert_loc)}
        else:
            rootpos[root] = (xcenter, vert_loc)
        if leafpos is None:
            leafpos = {}
        children = list(G.neighbors(root))
        leaf_count = 0
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            rootdx = width / len(children)
            nextx = xcenter - width / 2 - rootdx / 2
            for child in children:
                nextx += rootdx
                rootpos, leafpos, newleaves = _hierarchy_pos(G, child, leftmost + leaf_count * leafdx,
                                                             width=rootdx, leafdx=leafdx,
                                                             vert_gap=vert_gap, vert_loc=vert_loc - vert_gap,
                                                             xcenter=nextx, rootpos=rootpos, leafpos=leafpos,
                                                             parent=root)
                leaf_count += newleaves

            leftmostchild = min((x for x, y in [leafpos[child] for child in children]))
            rightmostchild = max((x for x, y in [leafpos[child] for child in children]))
            leafpos[root] = ((leftmostchild + rightmostchild) / 2, vert_loc)
        else:
            leaf_count = 1
            leafpos[root] = (leftmost, vert_loc)
        #        pos[root] = (leftmost + (leaf_count-1)*dx/2., vert_loc)
        #        print(leaf_count)
        return rootpos, leafpos, leaf_count

    xcenter = width / 2.
    if isinstance(G, nx.DiGraph):
        leafcount = len([node for node in nx.descendants(G, root) if G.out_degree(node) == 0])
    elif isinstance(G, nx.Graph):
        leafcount = len([node for node in nx.node_connected_component(G, root) if G.degree(node) == 1 and node != root])
    rootpos, leafpos, leaf_count = _hierarchy_pos(G, root, 0, width,
                                                  leafdx=width * 1. / leafcount,
                                                  vert_gap=vert_gap,
                                                  vert_loc=vert_loc,
                                                  xcenter=xcenter)
    pos = {}
    for node in rootpos:
        pos[node] = (
        leaf_vs_root_factor * leafpos[node][0] + (1 - leaf_vs_root_factor) * rootpos[node][0], leafpos[node][1])
    #    pos = {node:(leaf_vs_root_factor*x1+(1-leaf_vs_root_factor)*x2, y1) for ((x1,y1), (x2,y2)) in (leafpos[node], rootpos[node]) for node in rootpos}
    xmax = max(x for x, y in pos.values())
    for node in pos:
        pos[node] = (pos[node][0] * width / xmax, pos[node][1])
    return pos

def main():
    rabbit_mq_worker: RabbitMQWorker = None
    samba_worker: SambaWorker = None
    try:
        rabbit_mq_worker: RabbitMQWorker = RabbitMQWorker(rabbitMqConfig)
        samba_worker: SambaWorker = SambaWorker(sambaConfig)
        samba_worker.connect()

        config = rabbitMqConfig.INPUT_VERIFICATION_DOCUMENT_CONFIG
        consumer = VerifyDocumentConsumer(rabbit_mq_config=rabbitMqConfig, queue=config.get("queue"),
                            routing_key=config.get("routingKey"),
                            exchange=config.get("exchange"), samba_worker=samba_worker)
        rabbit_mq_worker.add_consumer(consumer)

        config = rabbitMqConfig.INPUT_NORMALIZE_DATA_CONFIG
        consumer = NormalizationDataConsumer(rabbit_mq_config=rabbitMqConfig, queue=config.get("queue"),
                                          routing_key=config.get("routingKey"),
                                          exchange=config.get("exchange"), samba_worker=samba_worker)
        rabbit_mq_worker.add_consumer(consumer)

        config = rabbitMqConfig.INPUT_REPORT_CONFIG
        consumer = ReportResultConsumer(
            rabbit_mq_config=rabbitMqConfig, queue=config.get("queue"),
            routing_key=config.get("routingKey"),
            exchange=config.get("exchange"), samba_worker=samba_worker
        )
        rabbit_mq_worker.add_consumer(consumer)

        rabbit_mq_worker.run()


    except KeyboardInterrupt:
        pass
    except BaseException as error:
        traceback.print_exc()
        LOGGER.exception(error)

    finally:
        if rabbit_mq_worker is not None:
            rabbit_mq_worker.close_connection()
        if samba_worker is not None:
            samba_worker.close()

    # jsonReport = ''
    # with open('../resources/test.json') as f:
    #     jsonReport = f.read()
    #
    # decoded_body: dict = json.loads(jsonReport)
    #
    # experiment_result_id = decoded_body.get("experimentResultId")
    # model: dict = decoded_body.get("model")
    #
    # neuronsLayers: list = model.get("neuronsLayers")
    # connections: list = model.get("connections")
    #
    # nodes: dict = {};
    # layer: list
    # G = nx.Graph()
    # neuron: dict
    # edges = []
    #
    # freeId = -1
    #
    # for layer in neuronsLayers:
    #     for neuron in layer:
    #         freeId = max(neuron.get("id"), freeId)
    #
    # level = 0
    # for layer in neuronsLayers:
    #     level += 1
    #     for neuron in layer:
    #         G.add_node(neuron.get("id"),
    #                    label=neuron.get("activationFunction"),
    #                    title=str(neuron.get("bias"))),
    #
    #         G.nodes.get(neuron.get("id"))["color"] = "blue" if neuron.get("type") == "INPUT" else "green" if neuron.get(
    #             "type") == "OUTPUT" else "orange"
    #         G.nodes.get(neuron.get("id"))["level"] = level
    #         if neuron.get("type") == "INPUT":
    #             freeId += 1
    #             G.add_node(freeId,
    #                        label=neuron.get("label"),
    #                        )
    #             G.nodes.get(freeId)["color"] = "transparent"
    #             G.nodes.get(freeId)["shape"] = "box"
    #             G.nodes.get(freeId)["level"] = level - 1
    #             G.nodes.get(freeId)["widthConstraint"] = {
    #                 "minimum": 10,
    #                 "maximum": 200
    #             }
    #             edges.append((neuron.get("id"), freeId))
    #         elif neuron.get("type") == "OUTPUT":
    #             freeId += 1
    #             G.add_node(freeId,
    #                        label=neuron.get("label"))
    #             G.nodes.get(freeId)["color"] = "transparent"
    #             G.nodes.get(freeId)["shape"] = "box"
    #             G.nodes.get(freeId)["widthConstraint"] = {
    #                 "minimum": 10,
    #                 "maximum": 200
    #             }
    #             G.nodes.get(freeId)["level"] = level + 1
    #             edges.append((freeId, neuron.get("id")))
    #         # node = pydot.Node(neuron.get("id"))
    #         # nodes[neuron.get("id")] = node
    #         # G.add_node(node)
    #
    # connection: dict
    #
    # for connection in connections:
    #     edges.append((connection.get("fromId"), connection.get("toId")))
    #
    # G.add_edges_from(edges)
    #
    # # G2 = Network(directed=True, layout={"hierarchical": {
    # #     "enabled": True,
    # #     "direction": 'LR',
    # #     "parentCentralization": True,
    # #     "edgeMinimization": True,
    # #     "treeSpacing": 200,
    # #     "nodeSpacing": 250,
    # #     "levelSeparation": 200,
    # #     "blockShifting": True
    # # }
    # # }, width="70%", height="100%")
    # #
    # #
    # # G2.show_buttons(filter_= "physics")
    # # G2.from_nx(G)
    #
    #  # G2.show("network.html")
    #
    #
    #
    # nx.draw(G, pos=hierarchy_pos(G,1) ,with_labels=True, )
    # plt.show(block=False)
    #plt.savefig("Graph.png", format="PNG")


# dataset_verification = DatasetVerificationPandas()
# dataset_verification.verify_excel(correct_file)
# legend_error_protocol, legend_info_protocol, legend_inc, headers_error_protocol, legend_header, \
# data_headers, values_error_protocol, legend_info_protocol, dataframe_to_save = dataset_verification.verify_excel(file_date_empty)
# #dataset_verification.verify_excel(file_number_empty)

if __name__ == "__main__":
    main()


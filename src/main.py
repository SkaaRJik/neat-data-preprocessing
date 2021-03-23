
from src.excel.verification.dataset_verification_pandas import DatasetVerificationPandas


def main():
	correct_file = '../resources/data.xlsx'
	file_date_empty = '../resources/data1.xlsx'
	file_number_empty = '../resources/data2.xlsx'
	dataset_verification = DatasetVerificationPandas()
	#dataset_verification.verify_excel(correct_file)
	legend_error_protocol, legend_info_protocol, legend_inc, headers_error_protocol, legend_header, \
	data_headers, values_error_protocol, legend_info_protocol, dataframe_to_save = dataset_verification.verify_excel(file_date_empty)
	#dataset_verification.verify_excel(file_number_empty)

if __name__ == "__main__":
	main()
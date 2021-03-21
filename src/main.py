
from src.excel.verification.dataset_verification_pandas import DatasetVerificationPandas


def main():
	file = 'F:/PythonProjects/neat-data-preprocessing/resources/data.xlsx'
	dataset_verification = DatasetVerificationPandas()
	dataset_verification.verify_excel(file)

if __name__ == "__main__":
	main()
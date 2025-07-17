from langchain.document_loaders import PyPDFLoader, DirectoryLoader, UnstructuredURLLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings


#Extract Data From the PDF File
def load_pdf_file(data):
    loader= DirectoryLoader(data,
                            glob="*.pdf",
                            loader_cls=PyPDFLoader)

    documents=loader.load()

    return documents
#Load data from coptic website
def load_data_from_url():
    urls = ['https://copticmission.org/medical-services/coptic-hospital',
            'https://copticmission.org/medical-services/coptic-hope-center-infectious-diseases',
            'https://copticmission.org/medical-services/medical-services',
            'https://copticmission.org/spiritual-services/discipleship'
            'https://coptichospitals.com/contact',
            'https://coptichospitals.com/about',
            'https://copticmission.org/humanitarian-services/coptic-school'
        
        ]
    
    loader_url = UnstructuredURLLoader(urls=urls)
    data_url = loader_url.load()
    
    return data_url
#Load csv and pdfs
def load_csv_and_pdf_files(datan):
    print(f"Loading data from: {datan}")
    
    # Load PDF files
    pdf_loader = DirectoryLoader(
        datan,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )
    print('Loading from PDF...')
    pdf_documents = pdf_loader.load()

    # Load CSV files
    csv_loader = DirectoryLoader(
        datan,
        glob="*.csv",
        loader_cls=CSVLoader
    )
    print('Loading from CSV...')
    csv_documents = csv_loader.load()
    
    print('Loading from URL...')
    url_data = load_data_from_url()

    # Combine documents
    all_documents = pdf_documents + csv_documents + url_data
    return all_documents



extracted_all_data = load_csv_and_pdf_files(datan='data/')

#Split the Data into Text Chunks
def text_split(extracted_all_data):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    text_chunks=text_splitter.split_documents(extracted_all_data)
    return text_chunks



#Download the Embeddings from HuggingFace 
def download_hugging_face_embeddings():
    embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')  #this model return 384 dimensions
    return embeddings
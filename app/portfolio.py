import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas=[{"links": row["Links"]}],
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        # Normalize skills to a non-empty list of strings
        if skills is None:
            raise ValueError("No skills found to query portfolio.")
        if isinstance(skills, str):
            skills_list = [skills] if skills.strip() else []
        elif isinstance(skills, list):
            skills_list = [str(s) for s in skills if str(s).strip()]
        else:
            raise ValueError("Skills must be a string or a list of strings.")

        if not skills_list:
            raise ValueError("No skills found to query portfolio.")

        return self.collection.query(query_texts=skills_list, n_results=2).get('metadatas', [])
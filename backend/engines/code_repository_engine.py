from providers.code_repository_provider import CodeRepositoryProvider

from providers.code_storage_provider import CodeStorageProvider

from engines.code_engine import CodeEngine


class CodeRepositoryEngine:

    def __init__(self):

        self.provider = CodeRepositoryProvider()

        self.storage = CodeStorageProvider()

        self.engine = CodeEngine()

    def compare(self, uploaded_path):

        uploaded_code = self.provider.extract(

            uploaded_path

        )

        repository = self.provider.get_all_documents()

        if len(repository) == 0:

            self.storage.save(uploaded_path)

            return {

                "repository_size": 0,

                "highest_similarity": 0,

                "matched_file": None,

                "matches": []

            }

        matches = []

        for document in repository:

            repository_code = self.provider.extract(

                document["path"]

            )

            result = self.engine.compare(

                uploaded_code,

                repository_code

            )

            matches.append({

                "file": document["name"],

                "similarity": result["overall_similarity"],

                "details": result

            })

        matches.sort(

            key=lambda x: x["similarity"],

            reverse=True

        )

        self.storage.save(uploaded_path)

        return {

            "repository_size": len(repository),

            "highest_similarity": matches[0]["similarity"],

            "matched_file": matches[0]["file"],

            "matches": matches

        }

    def documents(self):

        return self.storage.list_documents()

    def delete(self, filename):

        return self.storage.delete(filename)
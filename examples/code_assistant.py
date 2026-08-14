import ell
import ell
from git import Repo
class CodeAssistant:
    def __init__(self):
        ell.init(verbose=True, store='./logdir', autocommit=False)
        self.version = 0

    @ell.simple(model="gpt-4o-mini")
    def create_code(self, task: str, language: str):
        """You are an expert software engineer. Create code based on the given task and language."""
        return f"Create {language} code for the following task: {task}"

    @ell.simple(model="gpt-4o-mini")
    def review_code(self, code: str):
        """You are a code reviewer. Provide suggestions and improvements for the given code."""
        return f"Review the following code and provide suggestions:\n{code}"

    @ell.simple(model="gpt-4o-mini")
    def fix_code(self, code: str, suggestions: str):
        """You are a code fixer. Improve the code based on the given suggestions."""
        return f"Fix the following code based on these suggestions:\nCode:\n{code}\n\nSuggestions:\n{suggestions}"

    def save_draft(self, code: str):
        self.version += 1
        with open(f"draft_{self.version}.py", "w") as f:
            f.write(code)

    def git_commit(self, message: str):
        repo = Repo('.')
        repo.git.add(A=True)
        repo.index.commit(message)

    def run(self):
        task = input("Enter the coding task: ")
        language = input("Enter the programming language: ")

        code = self.create_code(task, language)
        print("\nInitial Code:")
        print(code)

        self.save_draft(code)
        self.git_commit(f"Initial code draft - version {self.version}")

        while True:
            review = self.review_code(code)
            print("\nCode Review:")
            print(review)

            user_input = input("\nDo you want to fix the code? (y/n): ")
            if user_input.lower() != 'y':
                break

            fixed_code = self.fix_code(code, review)
            print("\nFixed Code:")
            print(fixed_code)

            self.save_draft(fixed_code)
            self.git_commit(f"Code revision - version {self.version}")

            code = fixed_code

        print("\nFinal Code:")
        print(code)

if __name__ == "__main__":
    assistant = CodeAssistant()
    assistant.run()

from modules.core.models.files import File

class FileHelper:
    @staticmethod
    def print_order(files:list[File]):
        """Prints the file order"""
        for file in files:
            print(file.name,end="")
            print(" > ",end="")
    
    @staticmethod
    def get_next_unprocessed_file_index(files:list[File]) -> int:
        """Finds the index of the next file that has not been generated."""
        for index, file in enumerate(files):
            if not file.is_generated:
                return index
        return -1
    
    @staticmethod
    def get_last_generated_file_index(files:list[File]) -> int:
        """Finds the index of the most recently generated file."""
        for index in range(len(files) - 1, -1, -1):
            if files[index].is_generated:
                return index
        return -1


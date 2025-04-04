from modules.types.project_structure import File

class FileHelper:
    @staticmethod
    def pretty_print_files(files: list[File]) -> None:
        """
        Prints a formatted folder/file tree structure from a FilesList object.
        
        Args:
            files_list (FilesList): Pydantic model containing list of File objects
        """
        # Dictionary to store the folder structure
        tree = {}
        
        # Build the tree structure
        for file in files:
            current_level = tree
            # Split path into parts and clean it
            path_parts = file.path.strip('/').split('/')
            
            # Handle each part of the path
            for part in path_parts[:-1]:  # Exclude the filename
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
            
            # Add the file with its purpose
            current_level[path_parts[-1]] = {
                'name': file.name,
                'purpose': file.purpose
            }
    
        def print_tree(structure, prefix=""):
            """
            Recursive helper function to print the tree
            """
            items = sorted(structure.items())
            for index, (key, value) in enumerate(items):
                is_last = index == len(items) - 1
                connector = "└── " if is_last else "├── "
                
                if isinstance(value, dict) and 'name' in value:  # It's a file
                    print(f"{prefix}{connector}{value['name']}")
                    print(f"{prefix}{'    ' if is_last else '│   '}└── Purpose: {value['purpose']}")
                else:  # It's a directory
                    print(f"{prefix}{connector}{key}/")
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    print_tree(value, new_prefix)
        
        # Print the tree starting from root
        print("Project File Structure:")
        print_tree(tree)

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


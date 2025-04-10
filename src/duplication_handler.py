import os

from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True



class DuplicationHandler:
    @staticmethod
    def are_hashes_equal(hash_1, hash_2):
        return hash_1 == hash_2

    # return (hash_1 - hash_2)<10

    def remove_duplicate_images_by_hash(self, directory, path_images, hash_images, count_images):
        duplicate_dir = os.path.join(directory, "Duplicate")
        os.makedirs(duplicate_dir, exist_ok=True)
        duplicates_count = 0

        i, j = 0, 0

        while (i < len(hash_images)):
            j = i + 1
            while (j < len(hash_images)):
                if (self.are_hashes_equal(hash_images[i], hash_images[j])):
                    duplicates_count += 1
                    new_path_image = duplicate_dir + path_images[j][path_images[j].rfind('\\'):]
                    os.replace(path_images[j], new_path_image)
                    hash_images.pop(j)
                    path_images.pop(j)

                else:
                    j += 1
            i += 1

        return duplicates_count

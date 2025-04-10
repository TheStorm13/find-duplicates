import os
from alive_progress import alive_bar
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

class DuplicationHandler:
    def isDuplicateHash(self,hash_1, hash_2):
        return hash_1 == hash_2
    # return (hash_1 - hash_2)<10


    def deleteDublicatedImagesHash(self, directory, path_images, hash_images, count_images):
        directory_dublicate = directory + r"\Duplicate"
        os.makedirs(directory_dublicate, exist_ok=True)
        count_dublicate = 0
        i, j = 0, 0
        with alive_bar(count_images, title="Ищем дубликаты              ") as bar:
            while (i < len(hash_images)):
                j = i + 1
                while (j < len(hash_images)):
                    if (self.isDuplicateHash(hash_images[i], hash_images[j])):
                        count_dublicate += 1
                        new_path_image = directory_dublicate + path_images[j][path_images[j].rfind('\\'):]
                        os.replace(path_images[j], new_path_image)
                        hash_images.pop(j)
                        path_images.pop(j)
                        bar()
                    else:
                        j += 1
                i += 1
                bar()
        return count_dublicate
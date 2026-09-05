class Utils:
    @staticmethod
    def is_allowed_image_extension(filename: str) -> bool:
        return "." in filename and \
            filename.rsplit(".", 1)[1].lower() in ["jpeg"]

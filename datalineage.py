
class DataTracker:
    '''
    Generate ID for data run
    Save selected scripts in a folder with ID name
    Output ID so user-code can put data in folder
    '''

    def __init__(self, ID=None, name=None):
        self.ID = ID
        self.name = name
        
    def track(self, files, prefix=None):
        if prefix is not None:
            files = [prefix + f for f in files]
        if self.ID is None:
            self.genid()
        import shutil
        import os
        foldername = self.ID
        if self.name is not None:
            foldername = foldername + self.name

        if not os.path.exists(foldername):
            os.mkdir(foldername)
        else:
            raise ValueError("Folder {} already exists".format(foldername))

        cwd = os.getcwd()
        for fname in files:
            filename = self.replacedoubledots(fname)
            if not os.path.exists(filename):
                raise ValueError("File didnt exist: {}".format(filename))

            newname = filename.replace("/", ".")
            if newname.startswith("."):
                newname = newname[1:]
            

            shutil.copy2(filename, cwd + "/" + foldername + "/" + newname)
        
        import datetime
        datestamp = str(datetime.datetime.now()).replace(" ", "_")
        with open(cwd + "/" + foldername + "/" + datestamp + ".txt", "w+") as f:
            f.write(datestamp)

        return self.ID

    def genid(self):
        import uuid
        self.ID = str(uuid.uuid4())
        return self.ID

    def replacedoubledots(self, fname):
        import os
        cwd = os.getcwd()
        cwd = cwd.split("/")
        
        num_steps_up = fname.count("..")
        if num_steps_up == 0:
            return os.getcwd() + "/" + fname

        new_wd = cwd[:-num_steps_up]
        
        newfilename = fname.split("../")
        newfilename = [f for f in newfilename if f != ".." and f != "" and f != "/"]

        newfilename = "/".join(newfilename)
        new_wd.append(newfilename)
        
        return "/".join(new_wd)
        

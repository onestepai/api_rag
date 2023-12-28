import os
import zipfile
import shutil
import errno
from ServiceStepAI.FlaskServiceBase.ServiceApiConfigBase import ServiceApiConfigBase


class SystemUtil(object):
    @staticmethod
    def zipdir(dirPath=None, zipFilePath=None, includeDirInZip=False):
        """
        Attribution:  I wish I could remember where I found this on the
        web.  To the unknown sharer of knowledge - thank you.

        Create a zip archive from a directory.

        Note that this function is designed to put files in the zip archive with
        either no parent directory or just one parent directory, so it will trim any
        leading directories in the filesystem paths and not include them inside the
        zip archive paths. This is generally the case when you want to just take a
        directory and make it into a zip file that can be extracted in different
        locations.

        Keyword arguments:

        dirPath -- string path to the directory to archive. This is the only
        required argument. It can be absolute or relative, but only one or zero
        leading directories will be included in the zip archive.

        zipFilePath -- string path to the output zip file. This can be an absolute
        or relative path. If the zip file already exists, it will be updated. If
        not, it will be created. If you want to replace it from scratch, delete it
        prior to calling this function. (default is computed as dirPath + ".zip")

        includeDirInZip -- boolean indicating whether the top level directory should
        be included in the archive or omitted. (default False)
        """

        if not zipFilePath:
            zipFilePath = dirPath + ".zip"
        if not os.path.isdir(dirPath):
            raise OSError("dirPath argument must point to a directory. "
                          "'%s' does not." % dirPath)
        parentDir, dirToZip = os.path.split(dirPath)

        # Little nested function to prepare the proper archive path
        def trimPath(path):
            archivePath = path.replace(parentDir, "", 1)
            if parentDir:
                archivePath = archivePath.replace(os.path.sep, "", 1)
            if not includeDirInZip:
                archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1)
            return os.path.normcase(archivePath)

        outFile = zipfile.ZipFile(zipFilePath, "w",
                                  compression=zipfile.ZIP_DEFLATED)
        for (archiveDirPath, dirNames, fileNames) in os.walk(dirPath):
            for fileName in fileNames:
                filePath = os.path.join(archiveDirPath, fileName)
                outFile.write(filePath, trimPath(filePath))
            # Make sure we get empty directories as well
            if not fileNames and not dirNames:
                zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
                # some web sites suggest doing
                # zipInfo.external_attr = 16
                # or
                # zipInfo.external_attr = 48
                # Here to allow for inserting an empty directory.  Still TBD/TODO.
                outFile.writestr(zipInfo, "")
        outFile.close()

    @staticmethod
    def unzip(path_to_zip_file, directory_to_extract_to):
        if not os.path.exists(directory_to_extract_to):
            os.makedirs(directory_to_extract_to)
        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(directory_to_extract_to)

    @staticmethod
    def split_big_file(file_name, chunk_size, out_file_part_name):
        temp_dir = './temp'
        out_file_name_prefix = temp_dir + '/' + out_file_part_name + '_'
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)
        out_file_names = []
        file_size = SystemUtil.get_file_size(file_name)
        if file_size <= chunk_size:
            out_file_name = out_file_name_prefix + '1'
            shutil.copyfile(file_name, out_file_name)
            out_file_names.append(out_file_name)
            return out_file_names
        file_number = 1
        with open(file_name, 'rb') as f:
            chunk = f.read(chunk_size)
            while chunk:
                out_file_name = out_file_name_prefix + str(file_number)
                with open(out_file_name, 'wb') as chunk_file:
                    chunk_file.write(chunk)
                out_file_names.append(out_file_name)
                file_number += 1
                chunk = f.read(chunk_size)
        return out_file_names

    @staticmethod
    def delete_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            ServiceApiConfigBase.onestep_ai_logger.info("delete file: {}".format(file_path))
        else:
            ServiceApiConfigBase.onestep_ai_logger.warning("The file does not exist: {}".format(file_path))

    @staticmethod
    def delete_folder(folder_path):
        shutil.rmtree(folder_path, ignore_errors=True)
        ServiceApiConfigBase.onestep_ai_logger.info("delete folder: {}".format(folder_path))

    @staticmethod
    def get_file_size(file_path):
        statinfo = os.stat(file_path)
        return statinfo.st_size

    @staticmethod
    def copy_folder(src, dest):
        try:
            shutil.copytree(src, dest)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(src, dest)
            else:
                ServiceApiConfigBase.onestep_ai_logger.error('Directory not copied. Error: %s' % e)


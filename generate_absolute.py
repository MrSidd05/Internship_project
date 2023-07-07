from ast import parse
from genericpath import exists
from msilib import schema
from pydoc import describe
import os,argparse,os.path
import re

group=argparse.ArgumentParser(description="This show the contents of the file")
group.add_argument('filename',type=argparse.FileType('r'))
# group = my_parser.add_argument_group()
group.add_argument('-sc','--schema',type=str,action="store",help='This store the name of the folder',required=False)
group.add_argument('-c','--crud',action="store",type=str,help="This store the name of the folder",required=False)
group.add_argument('-s','--services',action="store",type=str,help="This store the name of the folder",required=False)

args=group.parse_args()


def CreateSchema():

    fileopen=open(args.filename.name,'r')
    read_content=fileopen.read()
    
    pattern=re.compile(r"class\s*([a-zA-Z]+)\(?")
    for match_class in pattern.finditer(read_content):
        matching_classname=match_class.group(1)

    if os.path.exists(args.schema):
        pass
    else:
        store_path_name=args.schema
        os.mkdir(os.path.abspath(store_path_name))
    
        write_file=open(f'{store_path_name}/master_data.py','w')
        str_file="""
from pydantic import BaseModel
class classnameCreateSchema(BaseModel):
    pass
class classnameUpdateSchema(BaseModel):
    pass
class classnameSchema(BaseModel):
    class Config:
        orm_mode = True
    """
        new_file=re.sub(pattern="classname",repl=matching_classname,string=str_file)
        write_file.write(new_file)
    
CreateSchema()



def CreateCrud():

    fileopen=open(args.filename.name,'r')
    read_content=fileopen.read()
    
    pattern=re.compile(r"class\s*([a-zA-Z]+)\(?")
    for match_class in pattern.finditer(read_content):
        matching_classname=match_class.group(1)

    if os.path.exists(args.crud):
        pass
    else:
        store_pathname=args.crud
        os.mkdir(os.path.abspath(store_pathname))

    write_file_crud=open(f'{store_pathname}/crud_entity_name.py','w')
    string_crud="""
from dde_core.orm import CRUDBase
import models.master_data as models
import schemas.master_data as schemas

class CURDclassname(
    CRUDBase[
        models.classname,
        schemas.classnameCreateSchema,
        schemas.classnameUpdateSchema,
    ]
):
    pass
crud_master_data = CURDclassname(models.classname)
    """
    new_file_crud=re.sub(pattern="classname",repl=matching_classname,string=string_crud)
    write_file_crud.write(new_file_crud)
    write_file_crud.close()

CreateCrud()




def CreateServices():

    fileopen=open(args.filename.name,'r')
    read_content=fileopen.read()
    
    pattern=re.compile(r"class\s*([a-zA-Z]+)\(?")
    for match_class in pattern.finditer(read_content):
        matching_classname=match_class.group(1)


    if os.path.exists(args.services):
        pass
    else:
        store_pathname=args.services
        os.mkdir(os.path.abspath(store_pathname))
    
    write_file_service= open(f'services/master_data_service.py','w')
    str_service="""
from logging import getLogger
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from schemas.master_data import (
    classnameCreateSchema,
    classnameSchema,
    classnameUpdateSchema,
)
from crud.crud_entity_name import crud_master_data


logger = getLogger(__name__)


class classnameService:
    def __init__(self, session: Session) -> None:
        self.session = session


    def get(self, id: int) -> Optional[classname]:
        logger.info(f"Fetching master data with id: {id}")
        return crud_master_data.get(
            self.session, id
        )

    def create(self, data: classnameCreateSchema) -> classname:
        return crud_master_data.create(self.session, data)

    def update(self, id: int, data: classnameUpdateSchema) -> classname:
        master_data = self.get(id)
        return crud_master_data.create(self.session, master_data, data)

    def delete(self, id: int) -> classname:
        return crud_master_data.remove(self.session, id)
    """
    new_fileservice=re.sub(pattern="classname",repl=matching_classname,string=str_service)
    write_file_service.write(new_fileservice)
    write_file_service.close()



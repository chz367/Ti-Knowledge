from InformationExtract.ELSEVIER_NEW import formElsevierNewTripleGroup
from InformationExtract.ELSEVIER_OLD import formElsevierOldTripleGroup
from InformationExtract.CRYSTALS import formCrystalsTripleGroup
from InformationExtract.MATERIAL_RESEARCH import formMRTripleGroup
from InformationExtract.MATERIAL_SCIENCE_FORUM import formMSFTripleGroup
from InformationExtract.OPTO_ELECTRONIC_ADVANCES import formOptoTripleGroup
from InformationExtract.POWDER_METALLURGY import formPMTripleGroup

def getArticleInfo(file_path, journal_type):
    # 根据文件类型调用不同的文献解析方法
    if journal_type == 'ELSEVIER_NEW':
        return formElsevierNewTripleGroup(file_path[:-4])
    elif journal_type == 'ELSEVIER_OLD':
        return formElsevierOldTripleGroup(file_path[:-4])
    elif journal_type == 'CRYSTALS':
        return formCrystalsTripleGroup(file_path[:-4])
    elif journal_type == 'MATERIALS_RESEARCH':
        return formMRTripleGroup(file_path[:-4])
    elif journal_type == 'MATERIALS_SCIENCE_FORUM':
        return formMSFTripleGroup(file_path[:-4])
    elif journal_type == 'OPTO_ELECTRONIC_ADVANCES':
        return formOptoTripleGroup(file_path[:-4])
    elif journal_type == 'POWDER_METALLURGY':
        return formPMTripleGroup(file_path[:-4])
    
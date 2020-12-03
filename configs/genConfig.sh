#!/bin/bash
BASE=$(pwd)
FILENAME_CONF="$BASE/routineValidator.properties"

OPTION=$1






if [ "$OPTION" == "-h" ] || [ "$OPTION" == "--help" ]; then
    echo ""
    echo "$0 permite la generación de la configuración por defecto del script de routineValidator"
    echo "Ejecución: $0 -g <DEV|UAT|PRD>"
elif [ "$OPTION" == "-g" ] || [ "$OPTION" == "--generate" ]; then

    rm -rf $FILENAME_CONF 2> /dev/null

    echo "[GLOBAL]" >> $FILENAME_CONF
    echo "whenslimit = 20" >> $FILENAME_CONF
    echo "insertlimit = 0" >> $FILENAME_CONF
    echo "selectalltlimit = 0" >> $FILENAME_CONF    
    echo "selectalltpointlimit = 0" >> $FILENAME_CONF
    echo "selectainsideparenthesislimit = 0" >> $FILENAME_CONF
    echo "withslimit = 5" >> $FILENAME_CONF
    echo "joinsLimit = 5" >> $FILENAME_CONF
    echo "unionslimit = 5" >> $FILENAME_CONF
    echo "partitionlimit = 0" >> $FILENAME_CONF
    echo "caseslimit = 50" >> $FILENAME_CONF
    echo "mappingTypeBadQuerys={'SelectaInsideParenthesisLimit':'LIMIT_SELECT_IN','selectalltpointlimit':'LIMIT_SELECT_POINT_ALL','Selectalltlimit':'LIMIT_SELECT_ALL','InsertsLimit':'LIMIT_INSERTS','JoinsLimit':'LIMIT_JOINS','UnionsLimit':'LIMIT_UNIONS','WhensLimit':'LIMIT_WHEN','WithLimit':'LIMIT_WITH','PartitionLimit':'WITHOUT_PARTITION','CasesLimit':'LIMIT_CASE'}" >> $FILENAME_CONF
    echo "patternExtractSegment=from ,inner join ,left join ,right join ,left outer join ,right outer join ,full outer join ,cross join ,left anti join ,right anti join , where ">> $FILENAME_CONF
    echo "patternValidateSegment=year=">> $FILENAME_CONF
    echo "dataBasesRaw=s_apoyo_corporativo,s_apoyo_financiero,s_bam_apoyo_corporativo,s_bam_apoyo_financiero,s_bam_canales,s_bam_clientes,s_bam_productos,s_bana_apoyo_corporativo,s_bana_apoyo_financiero,s_bana_canales,s_bana_clientes,s_bana_productos,s_bani_apoyo_corporativo,s_bani_apoyo_financiero,s_bani_canales,s_bani_clientes,s_bani_productos,s_canales,s_clientes,s_informacion,s_integracion,s_productos">> $FILENAME_CONF

    ## REGEX

    echo "unilineComment=--[^\n]*\n" >> $FILENAME_CONF
    echo "MultilineComment=(?<=\/\*)(.*)(?=\*\/)|(?<=\/\*)([\s\S]*?)(?=\*\/)" >> $FILENAME_CONF
    echo "singleQuotedText=\"(['])(?:(?=(\\\\?))\2.)*?\1\"" >> $FILENAME_CONF
    echo "doubleQuotedText='([\"])(?:(?=(\\\\?))\2.)*?\1'" >> $FILENAME_CONF 
    echo "whenRegex=(?<=case)(.*?)(?=end as)" >> $FILENAME_CONF
    echo "selectPointAll=.*" >> $FILENAME_CONF
    echo "selectallRegex=(?<=select)(.*?)(?=from)" >> $FILENAME_CONF
    echo "selectInsideParenthesisRegex=(in\s\([\s\w\n\,\*\singleQuote\doubleQuote\+\-\%\.\t]*select)" >> $FILENAME_CONF

    . $FILENAME_CONF 2> /dev/null

fi

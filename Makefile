include .env


LOCALES_DIR := locales
LOCALES_DOMAIN := saver


update_lang:
	pybabel extract . -o ${LOCALES_DIR}/${LOCALES_DOMAIN}.pot
	pybabel update -d ${LOCALES_DIR} -D ${LOCALES_DOMAIN} -i ${LOCALES_DIR}/${LOCALES_DOMAIN}.pot


compile_lang:
	pybabel compile -d ${LOCALES_DIR} -D ${LOCALES_DOMAIN}

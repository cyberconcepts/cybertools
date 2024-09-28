# runtests.sh
# run all currently relevant unit / doc tests

zope-testrunner --test-path=. \
	-s cybertools.brain \
	-s cybertools.browser \
	-s cybertools.catalog \
	-s cybertools.commerce \
	-s cybertools.composer \
	-s cybertools.container \
	-s cybertools.docgen \
	-s cybertools.external \
	-s cybertools.integrator -t \!bscw \
	-s cybertools.knowledge \
	-s cybertools.link \
	-s cybertools.media \
	-s cybertools.meta \
	-s cybertools.organize \
	-s cybertools.process \
	-s cybertools.relation \
	-s cybertools.reporter \
	-s cybertools.stateful \
	-s cybertools.storage -t \!pzope \
	-s cybertools.text \
	-s cybertools.tracking \
	-s cybertools.typology \
	-s cybertools.util \
	$*

#-s cybertools.view \
#-s cybertools.wiki \

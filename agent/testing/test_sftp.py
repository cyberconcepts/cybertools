

from twisted.internet import reactor

from cybertools.agent.transport.file.sftp import FileTransfer

def output(x):
    print x

ft = FileTransfer('cy05.de', 22, 'scrat', 'pyjmfha')

d = ft.upload('d:\\text2.rtf', 'text.txt')
d.addCallback(output)

reactor.callLater(21, ft.close)
reactor.callLater(32, reactor.stop)

reactor.run()

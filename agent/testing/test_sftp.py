

from twisted.internet import reactor

from cybertools.agent.transport.file.sftp import FileTransfer

def output(x):
    print x

ft = FileTransfer('cy05.de', 22, 'scrat', '...')

d = ft.upload('d:\\text.txt', 'text.txt')
d.addCallback(output)

reactor.callLater(3, ft.close)
reactor.callLater(4, reactor.stop)

reactor.run()

#! /usr/bin/env python
#Based on http://pastebin.com/ZT4vk19r
 
import pexpect, os, re, time
 
class Server:
  """
 Spawn a server object with myServer = Server()
 and enter one of the following commands:
 
 myServer.start()           -- Starts the minecraft server
 myServer.stop()            -- Stops a currently running minecraft server
 myServer.status()          -- returns the status of the minecraft server
 myServer.command('string') -- Sends a command to the server and returns the next line
 myServer.message('string') -- Sends string as a server message
 myServer.players()         -- List of active players
 myServer.console(n)        -- display the last n lines of the console
 myServer.chat(n)           -- print the last n lines of chat history
 
 If there is already a server running, the instantiated server will resume it,
 if not, you can start one with myServer.start().
 
 The server is run in a screen with title "mc" so you can resume it from
 any terminal with the command: "screen -rd mc"
 """
 
 
  #Initialize the object
  def __init__(self):
    #Instance variables
    self.startupScript = os.path.expanduser('~') + '/craftbukkit/craftbukkit.sh'
   
    #Check the server status. If it is already running, resume it, if not, start it up.
    if self.status():
      print 'Resuming already running server.'
      self.mcServer = pexpect.spawn('screen -rd mc')
    else:
      print 'Server not running. Start with myServer.start()'
 
   
  #Start the server
  def start(self):
    print 'Starting server... ',
    if not self.status():
      self.mcServer = pexpect.spawn('screen -S mc ' + self.startupScript, timeout=120)
      self.mcServer.expect('\[INFO\] Done')
      print 'Started'
    else:
      print 'Server is already running'
 
  #Stop the server  
  def stop(self):
    print 'Stopping server... ',
    if self.status():
      self.mcServer.sendline('stop')
      self.mcServer.expect('\[screen is terminating\]')
      self.mcServer.kill
      print 'Stopped'
    else:
      print 'There is no server to stop.'
 
  #return the status of the server (True if server is on)
  def status(self):
    screenList = os.popen('screen -ls').read()
    match = re.search(r'\t\d+\.mc\t', screenList)
    if match:
      return True
    else:
      return False
     
  #Send a command to the server and (probably) return the next line
  def command(self, command, sleep=0.08):
    if self.status():
      self.mcServer.sendline(command)
      time.sleep(sleep)
      return self.console(1)[0]
    else:
      print 'There is no server running, start with myServer.start()'
   
  #Send message to players with /say command
  def message(self, messageString):
    if self.status():
      self.mcServer.sendline('say ' + messageString)
    else:
      print 'There is no server running, start with myServer.start()'
   
  #Return a list of active players
  def players(self):
    if self.status():
      out = self.command('list').split('\x1b[m')
      del out[-1]
      return out
    else:
      print 'There is no server running, start with myServer.start()'
   
  #Return a list the last n lines of the console stream. If numOfLines is specified,
  #only return that many lines starting from n lines back
  def console(self, n=10, numOfLines=0):
    bukkitDir = os.path.split(self.startupScript)[0]
    serverLogPath = os.path.join(bukkitDir, 'server.log')
    logFile = open(serverLogPath, 'r')
   
    bytesBack=0
    newLinePos = []
    #This loop reads in reverse from the end of the file looking for newline characters
    #When it finds n+1 charaters it knows it has gone back far enough for n lines
    while len(newLinePos) < n+1:
      bytesBack = bytesBack + 1
      logFile.seek(0-bytesBack, os.SEEK_END)
      if logFile.read(1) == '\n':
        newLinePos.append(bytesBack) #Store the position of each newline character
    logFile.seek(0-bytesBack, os.SEEK_END)
    if numOfLines is not 0: #Keep the 0 case as all of the lines
      numOfLines = numOfLines + 1
    logFileDump = logFile.read(bytesBack-newLinePos[0-numOfLines])
    logFileLines = logFileDump.split('\n')
    logFile.close()
    logFileLines.pop(0)  
    return logFileLines
   
  #Return the last n lines of chat history, if oneLine is set true, only return the nth line back
  def chat(self, n=10, oneLine = False):
    searchBack = 500
    chatLines = []
    while len(chatLines) < n+1:
      logLines = self.console(searchBack,500)
      for line in logLines:
        match = re.search(r'<\w+>', line)
        match2 = re.search(r'\[CONSOLE\]', line)
        if match or match2:
          chatLines.append(line)
      searchBack = searchBack + 500
    if oneLine is False:
      return sorted(chatLines)[-n:]
    else:
      return sorted(chatLines)[-n]
     
  #This method is very similar to the console method above, except it searches back until it reaches
  #a specific line specified by readToLine
  def consoleReadTo(self, readToLine):
    bukkitDir = os.path.split(self.startupScript)[0]
    serverLogPath = os.path.join(bukkitDir, 'server.log')
    logFile = open(serverLogPath, 'r')
         
    bytesBack=0
    newLinePos = []
    currentLine = ''
    #This loop reads in reverse from the end of the file looking for the specified line
    while readToLine != currentLine:
      bytesBack = bytesBack + 1
      logFile.seek(0-bytesBack, os.SEEK_END)
      if logFile.read(1) == '\n':
        newLinePos.append(bytesBack) #Store the position of each newline character
        if len(newLinePos)>1:
          currentLine = logFile.read((newLinePos[-1]-newLinePos[-2])-1)
    logFileDump = logFile.read(newLinePos[-2])
    logFileLines = logFileDump.split('\n')
    logFile.close()
    return logFileLines[0:-1]    
 
def main():
  print Server.__doc__
 
if __name__ == '__main__':
  main()

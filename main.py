import re

data = ["""
[producer * 10] 1:1-> [consumer * 10]
""",
"""
[producer * 10] 1:*-> [consumer * 10]
""",
"""
[producer * 10] *:1-> [consumer * 10]
""",
"""
[producer * 10] *:*-> [consumer * 10]
"""
 ]

class ParserError(BaseException):
  def __init__(self, message):
    super(ParserError, self).__init__(message)

class Parser:
  def __init__(self, data):
    self.data = data
    self.pos = 0
    self.end = False
    self.parsed = []
    self.last_char = ""
  def char(self):
    token = self.data[self.pos]
    if self.pos == len(self.data):
      self.end = True
    self.pos = self.pos + 1
    
    return token
  def token(self):
    while self.end == False and (self.last_char == " " or self.last_char == "\n" or self.last_char == ""):
      self.last_char = self.char()
      print("skipping whitespace")

    
    if self.last_char == "-":
      self.last_char = self.char()
      return "arrowstart"

    if self.last_char == ">":
      self.last_char = self.char()
      return "arrow"
    
    
    if self.last_char == "[":
      self.last_char = self.char()
      return "opensquare"
    if self.last_char == ":":
      self.last_char = self.char()
      return "separator"
    
    if self.last_char == "]":
      self.last_char = self.char()
      return "closesquare"
    if self.last_char == "*":
      self.last_char = self.char()
      return "multiply"

    match = re.match("[a-zA-Z]", self.last_char)
    if match:
      identifier = ""
      while re.match("[a-zA-Z]", self.last_char):
        identifier = identifier + self.last_char
        self.last_char = self.char()
      
      return identifier

    match = re.match("[0-9]", self.last_char)
    if match:
      identifier = ""
      while re.match("[0-9]", self.last_char):
        identifier = identifier + self.last_char
        self.last_char = self.char()
     
      return identifier
  
  def parse(self):
    start = self.token()
    print(start)
    if start == "opensquare":
      self.parse_list()
    else:
      lhs_relation = self.token()

    lhs = self.token()
    separator = self.token()
    rhs = self.token()
    print(lhs)
    print(separator)
    print(rhs)
    arrowstart = self.token()
    arrow = self.token()

    token = self.token()
    
    if token == "opensquare":
      self.parse_list()
    else:
      rhs_relation = self.token()

    if lhs == "multiply":
      lhs_times = int(self.parsed[0]["instances"])
    else:
      lhs_times = int(lhs)
    if rhs == "multiply":
      rhs_times = int(self.parsed[1]["instances"])
    else:
      rhs_times = int(rhs)
  
    print(lhs_times)
    print(rhs_times)
    
    for i in range(0, lhs_times):
      for j in range(0, rhs_times):
        print("{}{} -> {}{}".format(self.parsed[0]["name"], i if lhs_times > 1 else j, self.parsed[1]["name"], j if rhs_times > 1 else i))
    
    return self.parsed

  def parse_list(self):
    identifier = self.token()
    operator = self.token()
    number = self.token()
    print("encountered list")
    print(identifier)
    print(operator)
    print(number)
    close = self.token()
    if close != "closesquare":
      raise ParserError("error, expected close square was {}".format(close))
    self.parsed.append({
      "name": identifier,
      "instances": number
    })

def parse(item):
  print("####### {}".format(item))
  parser = Parser(item)
  return parser.parse()

for item in data:
  print(parse(item))
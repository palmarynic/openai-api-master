import os
from dotenv import load_dotenv

import  test
load_dotenv()


test.aa = os.getenv("ASSISTANT_ID")
print("id：", test.aa)


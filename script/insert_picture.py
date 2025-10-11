from sqlmodel import Session, create_engine
import os
from dotenv import load_dotenv
from db.models.fruit_model import Fruit
from db.models.vegetable_model import Vegetable

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = (   f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
                    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
 )


engine = create_engine(DATABASE_URL)

Data_Fruits = [

    {    #--Apple--
        "name": "Apple (แอปเปิ้ล)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Apple.jpg",
        "description":" จะมีรสหวานฉ่ำ เหมาะสำหรับทานสดหรือทำขนม ในขณะที่ แอปเปิลเขียว จะมีรสเปรี้ยวอมหวาน เนื้อแน่นกรอบ เหมาะสำหรับนำไปทำสลัดหรือขนม "
    },
    
     {    #--Avocado--
        "name": "Avocado (อะโวคาโด)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Avocado.jpg",
        "description":"อะโวคาโดสุกมีรสชาติอ่อนๆ มัน และหอมมันคล้ายเนยหรือถั่วเล็กน้อย เนื้อสัมผัสเนียนนุ่มครีมมี่ หากอะโวคาโดยังไม่สุกจะมีรสขมเพราะมีสารแทนนิน แต่หากสุกเกินไปจะมีรสชาติและกลิ่นที่ไม่ดี"
    },
    
     {    #--Banana--
        "name": "Banana (กล้วย)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Banana.jpg",
        "description":"กล้วยจะมีความหลากหลายขึ้นอยู่กับ ชนิด ระยะการสุก และ วิธีปรุง โดยทั่วไปกล้วยสุกจะมีรสหวาน หอม เนื้อนุ่มเหนียว ส่วนกล้วยดิบจะมีรสฝาด ปนหวานเล็กน้อย และนิยมนำไปทำอาหารคาว แต่ละสายพันธุ์ก็มีรสชาติเฉพาะตัว เช่น กล้วยน้ำว้าหวานอมเปรี้ยวเล็กน้อย กล้วยหอมจะมีกลิ่นหอมและรสหวานกลมกล่อม ส่วนกล้วยหักมุกมีรสหวานอมเปรี้ยวโดดเด่น นิยมนำไปย่าง "
    },
    
     {    #--Apple--
        "name": "Apple (แอปเปิ้ล)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Apple.jpg",
        "description":" จะมีรสหวานฉ่ำ เหมาะสำหรับทานสดหรือทำขนม ในขณะที่ แอปเปิลเขียว จะมีรสเปรี้ยวอมหวาน เนื้อแน่นกรอบ เหมาะสำหรับนำไปทำสลัดหรือขนม "
    },
    
     {    #--Apple--
        "name": "Apple (แอปเปิ้ล)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Apple.jpg",
        "description":" จะมีรสหวานฉ่ำ เหมาะสำหรับทานสดหรือทำขนม ในขณะที่ แอปเปิลเขียว จะมีรสเปรี้ยวอมหวาน เนื้อแน่นกรอบ เหมาะสำหรับนำไปทำสลัดหรือขนม "
    },
    
     {    #--Apple--
        "name": "Apple (แอปเปิ้ล)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Apple.jpg",
        "description":" จะมีรสหวานฉ่ำ เหมาะสำหรับทานสดหรือทำขนม ในขณะที่ แอปเปิลเขียว จะมีรสเปรี้ยวอมหวาน เนื้อแน่นกรอบ เหมาะสำหรับนำไปทำสลัดหรือขนม "
    },
    
     {    #--Apple--
        "name": "Apple (แอปเปิ้ล)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Apple.jpg",
        "description":" จะมีรสหวานฉ่ำ เหมาะสำหรับทานสดหรือทำขนม ในขณะที่ แอปเปิลเขียว จะมีรสเปรี้ยวอมหวาน เนื้อแน่นกรอบ เหมาะสำหรับนำไปทำสลัดหรือขนม "
    },
    
     {    #--Apple--
        "name": "Apple (แอปเปิ้ล)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Apple.jpg",
        "description":" จะมีรสหวานฉ่ำ เหมาะสำหรับทานสดหรือทำขนม ในขณะที่ แอปเปิลเขียว จะมีรสเปรี้ยวอมหวาน เนื้อแน่นกรอบ เหมาะสำหรับนำไปทำสลัดหรือขนม "
    },
    
     {    #--Apple--
        "name": "Apple (แอปเปิ้ล)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Apple.jpg",
        "description":" จะมีรสหวานฉ่ำ เหมาะสำหรับทานสดหรือทำขนม ในขณะที่ แอปเปิลเขียว จะมีรสเปรี้ยวอมหวาน เนื้อแน่นกรอบ เหมาะสำหรับนำไปทำสลัดหรือขนม "
    },
    
     {    #--Apple--
        "name": "Apple (แอปเปิ้ล)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Apple.jpg",
        "description":" จะมีรสหวานฉ่ำ เหมาะสำหรับทานสดหรือทำขนม ในขณะที่ แอปเปิลเขียว จะมีรสเปรี้ยวอมหวาน เนื้อแน่นกรอบ เหมาะสำหรับนำไปทำสลัดหรือขนม "
    },
    
     {    #--Apple--
        "name": "Apple (แอปเปิ้ล)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Apple.jpg",
        "description":" จะมีรสหวานฉ่ำ เหมาะสำหรับทานสดหรือทำขนม ในขณะที่ แอปเปิลเขียว จะมีรสเปรี้ยวอมหวาน เนื้อแน่นกรอบ เหมาะสำหรับนำไปทำสลัดหรือขนม "
    },
    
     {    #--Apple--
        "name": "Apple (แอปเปิ้ล)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Apple.jpg",
        "description":" จะมีรสหวานฉ่ำ เหมาะสำหรับทานสดหรือทำขนม ในขณะที่ แอปเปิลเขียว จะมีรสเปรี้ยวอมหวาน เนื้อแน่นกรอบ เหมาะสำหรับนำไปทำสลัดหรือขนม "
    },
    
     {    #--Apple--
        "name": "Apple (แอปเปิ้ล)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Apple.jpg",
        "description":" จะมีรสหวานฉ่ำ เหมาะสำหรับทานสดหรือทำขนม ในขณะที่ แอปเปิลเขียว จะมีรสเปรี้ยวอมหวาน เนื้อแน่นกรอบ เหมาะสำหรับนำไปทำสลัดหรือขนม "
    },
    
     {    #--Apple--
        "name": "Apple (แอปเปิ้ล)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Apple.jpg",
        "description":" จะมีรสหวานฉ่ำ เหมาะสำหรับทานสดหรือทำขนม ในขณะที่ แอปเปิลเขียว จะมีรสเปรี้ยวอมหวาน เนื้อแน่นกรอบ เหมาะสำหรับนำไปทำสลัดหรือขนม "
    },
    
     {    #--Apple--
        "name": "Apple (แอปเปิ้ล)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Apple.jpg",
        "description":" จะมีรสหวานฉ่ำ เหมาะสำหรับทานสดหรือทำขนม ในขณะที่ แอปเปิลเขียว จะมีรสเปรี้ยวอมหวาน เนื้อแน่นกรอบ เหมาะสำหรับนำไปทำสลัดหรือขนม "
    },
    
    
    
    
]
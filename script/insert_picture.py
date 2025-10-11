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
    
     {    #--Blackberry--
        "name": "Blackberry (แบล็คเบอรี่)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Blackberry.jfif",
        "description":"แบล็คเบอร์รี่มีรสชาติ เปรี้ยวอมหวาน มีกลิ่นหอมอ่อนๆ เนื้อฉ่ำน้ำและมีเมล็ดเล็กๆ อยู่ทั่วผล บางสายพันธุ์อาจมีรสฝาดเล็กน้อยจากสารแทนนิน เมื่อสุกเต็มที่จะมีรสชาติหวานเด่นขึ้น"
    },
    
     {    #--Cantaloupe--
        "name": "Cantaloupe (แคนตาลูป)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Cantaloupe.jpg",
        "description":"แคนตาลูปมีรสชาติ หวานฉ่ำ มีกลิ่นหอมเฉพาะตัว เนื้อแคนตาลูปมีทั้งสีส้ม สีเหลือง หรือเขียว ขึ้นอยู่กับพันธุ์นอกจากรสชาติอร่อยแล้ว ยังเป็นผลไม้ที่มีประโยชน์ต่อสุขภาพสูงโดยเฉพาะวิตามินเอและซีที่ช่วยบำรุงผิวพรรณและเสริมภูมิคุ้มกัน"
    },
    
     {    #--Cherry--
        "name": "Cherry (เชอรี่)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Cherry.jfif",
        "description":"เชอร์รี่มีรสชาติ หวานอมเปรี้ยว โดยรสชาติจะแตกต่างกันไปตามสายพันธุ์ บางชนิดจะหวานกว่า บางชนิดจะเปรี้ยวจี๊ดกว่า โดยทั่วไปเชอร์รี่ที่สุกแล้วจะมีเนื้อแน่น ฉ่ำ และมีความกรอบอร่อย"
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
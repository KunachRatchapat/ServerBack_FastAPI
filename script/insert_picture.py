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
    
     {    #--Corn--
        "name": "Corn (ข้าวโพด)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Corn.jfif",
        "description":"ข้าวโพดมีรสชาติหวานมัน และมีหลายประเภท เช่น ข้าวโพดหวานที่มีรสหวานตามธรรมชาติ, ข้าวโพดเทียนมีเนื้อสัมผัสเหนียว, และข้าวโพดนมสดฮอกไกโดที่มีรสหวานฉ่ำคล้ายนมสด"
    },
    
     {    #--Grape--
        "name": "Grape (องุ่น)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Grape.jpg",
        "description":" องุ่นมีรสชาติหลักๆ คือ หวานอมเปรี้ยว ซึ่งแต่ละสายพันธุ์จะมีรสชาติและเนื้อสัมผัสที่แตกต่างกันไป ตั้งแต่หวานสดชื่นไปจนถึงหวานหอมเข้มข้น มีหลายพันธุ์ที่ได้รับความนิยม เช่น องุ่นเคียวโฮ (หวานอมเปรี้ยว กลิ่นหอม), องุ่นไชมัสคัส (หวานเข้มข้น ฉ่ำน้ำ กลิ่นหอมเฉพาะตัว) หรือองุ่น Autumn Crisp (หวานอมเปรี้ยว เนื้อกรอบแน่น)"
    },
    
     {    #--Mango--
        "name": "Mango (มะม่วง)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Mango.jpg",
        "description":"รสชาติของมะม่วงมีหลากหลายตามสายพันธุ์และอายุ ตั้งแต่เปรี้ยวจัดในมะม่วงดิบไปจนถึงหวานจัดในมะม่วงสุก บางพันธุ์มีรสชาติเฉพาะตัว เช่น มัน หวาน กรอบ หรือ หวานอมเปรี้ยว"
    },
    
     {    #--Nut--
        "name": "Nut (ถั่ว)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Nut.jpg",
        "description":"รสชาติของถั่ว (Nut) มีหลากหลายขึ้นอยู่กับชนิดของถั่วและวิธีการปรุง โดยทั่วไปมีรส หวานมัน เป็นหลัก เช่น วอลนัทและพีแคน นอกจากนี้ยังมีรสชาติอื่นๆ ที่ได้จากการปรุง"
    },
    
     {    #--Orange--
        "name": "Orange (ส้ม)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Orange.jfif",
        "description":" รสชาติของส้มโดยทั่วไปคือ หวานอมเปรี้ยว พร้อมกลิ่นหอมสดชื่น แต่จะแตกต่างกันไปตามสายพันธุ์"
    },
    
     {    #--Papaya--
        "name": "Papaya (มะละกอ)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Papaya.jpg",
        "description":"มะละกอมีรสชาติที่แตกต่างกันไปตามความสุกและสายพันธุ์ โดยมะละกอสุกจะมีรส หวานหอม ส่วนมะละกอดิบจะมีรส จืดและกรอบ นอกจากนี้ ยังมีพันธุ์ที่ให้รสชาติเปรี้ยวอมหวาน เช่น มะละกอแขกนวล"
    },
    
     {    #--Pumpkin--
        "name": "Pumpkin (ฟักทอง)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Pumpkin.jfif",
        "description":"รสชาติของฟักทองจะ หวานมันและมีกลิ่นหอมเฉพาะตัว ซึ่งอาจแตกต่างกันไปตามสายพันธุ์ โดยทั่วไปฟักทองสุกจะมีเนื้อแน่นและนุ่ม มีทั้งรสหวานธรรมชาติหรือรสชาติเหมือนถั่วเล็กน้อยขึ้นอยู่กับพันธุ์"
    },
    
     {    #--Strawberry --
        "name": "Strawberry (สตรอเบอรี่)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Strawberry.jpg",
        "description":"สตรอว์เบอร์รีมีรสชาติโดยรวมคือ เปรี้ยวอมหวาน และ มีกลิ่นหอม เป็นเอกลักษณ์โดยรสชาติที่เด่นชัดนี้จะแตกต่างกันไปในแต่ละสายพันธุ์และแหล่งที่ปลูก"
    },
    
     {    #--Tomato--
        "name": "Tomato (มะเขือเทศ)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Fruits/Tomato.jpg",
        "description":"รสชาติของมะเขือเทศจะแตกต่างกันไปตามสายพันธุ์ โดยทั่วไปจะมีรส เปรี้ยวอมหวาน มะเขือเทศบางพันธุ์จะมีรสหวานจัด ในขณะที่บางพันธุ์จะรสเปรี้ยวเด่นบางสายพันธุ์จะมีรสชาติกลมกล่อม"
    },
    
]
    
    

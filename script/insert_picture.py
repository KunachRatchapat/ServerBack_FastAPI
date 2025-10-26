
from sqlmodel import Session, create_engine, select
import os
from dotenv import load_dotenv


from db.models.user_model import Users
from db.models.fruit_model import Fruit
from db.models.vegetable_model import Vegetable
from db.models.favorite_model import Favorite

from pydantic import BaseModel
from typing   import Optional


class FruitInput(BaseModel):
    name: str
    picture: str
    description: Optional[str]

class VegetableInput(BaseModel):
    name: str
    picture: str
    description: Optional[str]


load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
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

Data_Vegetables = [
     {    #--bean--
        "name": "Beans (ถั่ว)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Veggie/beans.png",
        "description":"รสชาติของถั่วมีความหลากหลายมาก ขึ้นอยู่กับประเภทของถั่ว, วิธีการปรุงและสายพันธุ์โดยทั่วไปถั่วจะมีรสชาติมัน หวานเล็กน้อย เค็ม"
    },
    
      {    #--Bell pepper--
        "name": "Bell-pepper (พริกหยวก)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Veggie/Bell-Peppers.jpg",
        "description":"พริกหยวกมีรสชาติหวาน มีเผ็ดเล็กน้อย ซึ่งระดับความเผ็ดจะแตกต่างกันไปตามสีของพริก โดยพริกหยวกสีเขียวจะเผ็ดที่สุด ส่วนสีเหลือง ส้ม และแดงจะค่อยๆ หวานขึ้นและเผ็ดน้อยลงตามลำดับ"
    },
    
      {    #--Bitter gourd--
        "name": "Bitter Gourd(มะระขี้นก)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Veggie/bitter-ground.jpg",
        "description":"มะระขี้นกมีรสขมจัด ซึ่งเป็นลักษณะเด่นที่ทำให้เป็นสมุนไพรที่มีสรรพคุณทางยา โดยเฉพาะอย่างยิ่งในการช่วยลดระดับน้ำตาลในเลือด"
    },
    
      {    #--Brocoli--
        "name": "Brocoli (บรอกโคลี)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Veggie/brocoli.jpeg",
        "description":" รสชาติของบรอกโคลีมีลักษณะเฉพาะตัวเป็นรสชาติแบบดินๆ มีความขมเล็กน้อย และเมื่อปรุงสุกแล้วจะให้รสชาติหวานกรอบ นอกจากนี้บรอกโคลียังมีกลิ่นเฉพาะตัวที่ค่อนข้างแรง โดยเฉพาะอย่างยิ่งเมื่อนำมาปรุงให้สุก"
    },
    
      {    #--Cabbage--
        "name": "Cabbage (กะหล่ำปลี)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Veggie/Cabbage.jpg",
        "description":"กะหล่ำปลีมีรสชาติพื้นฐาน หวานกรอบ แต่รสชาติจะแตกต่างกันไปตามสายพันธุ์และวิธีการปรุง โดยกะหล่ำปลีหัวใจจะมีรสหวานกว่ากะหล่ำปลีทั่วไป ส่วนกะหล่ำปลีม่วงอาจมีรสขมกว่ากะหล่ำปลีเขียวเล็กน้อย"
    },
    
      {    #--Carrot--
        "name": "Carrot (แครอท)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Veggie/Carrot.jpg",
        "description":"แครอทมีรสชาติหวาน เป็นหลัก โดยความหวานมาจากน้ำตาลธรรมชาติ เช่น กลูโคส ฟรุกโตส และบางครั้งอาจมีรสขมเล็กน้อย"
    },
    
      {    #--Cauliflower--
        "name": "Cauliflower (ดอกกะหล่ำ)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Veggie/Cauliflower.jpg",
        "description":"ดอกกะหล่ำมีรสชาติค่อนข้างอ่อน กลมกล่อม แทบจะไม่ขัดแย้งกับรสชาติอื่นเลย"
    },
    
      {    #--Cucumber--
        "name": "Cucumber (แตงกวา)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Veggie/Cucumber.jpeg",
        "description":"แตงกวามีรสชาติหวานน้อย กรุบกรอบ และสดชื่น"
    },
    
      {    #--Eggplant--
        "name": "Eggplant (มะเขือยาว)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Veggie/Eggplant.jpg",
        "description":"มะเขือยาวมีรสชาติอ่อนนุ่ม เมื่อปรุงสุกจะอร่อยกลมกล่อม"
    },
    
      {    #--lemon--
        "name": "lemon (เลมอน)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Veggie/lemon.jpg",
        "description":"เลมอนมีรสชาติ เปรี้ยวอมหวานซึ่งเป็นเอกลักษณ์จากกรดซิตริก แต่โดยรวมแล้วเปรี้ยวจัดกว่ามะนาว แต่จะมีความหวานและกลมกล่อมมากกว่า"
    },
    
      {    #--Onion--
        "name": "Onion (หอมใหญ่)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Veggie/Onnion.jfif",
        "description":"หอมหัวใหญ่มีรสชาติที่แตกต่างกันไปตามการปรุง โดยแบบดิบจะมีรสเผ็ดร้อนและฉุน ในขณะที่หากนำไปปรุงสุกรสชาติจะหวานขึ้นและกลิ่นฉุนจะลดลง"
    },
    
      {    #--Potato--
        "name": "Potato (มันฝรั่ง)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Veggie/Potato.jpg",
        "description":"มันฝรั่งจะมีหลายรสชาติและอยู่ที่การปรุง"
    },
    
      {    #--Zuchini--
        "name": "AppZuchini (ซูกินี)",
        "picture":"https://veggiepeak-fastapi-app-images.s3.ap-southeast-2.amazonaws.com/Veggie/Zuchini.jpg",
        "description":"ซูกินีมีรสชาติจืด ๆ คล้ายแตงกวาแต่มีความหวานกว่าเล็กน้อย และมีเนื้อสัมผัสที่นุ่มนวลเหมือนบวบสามารถทานได้ทั้งแบบสดและปรุง"
    },
    
]

def insert_data():
    with Session(engine) as session:
        print("Start Data Insertion/Update...")

        # --- Insert/Update Fruits ---
        for fruit_data in Data_Fruits:
            # 1. ค้นหาว่ามี Fruit นี้อยู่แล้วหรือไม่
            existing_fruit = session.exec(
                select(Fruit).where(Fruit.name == fruit_data["name"])
            ).first()

            # 2. ใช้ Pydantic Schema เป็นตัวกรอง (สำคัญในการรับประกันข้อมูลถูกต้อง)
            validated_data = FruitInput(**fruit_data)

            if existing_fruit:
                # ถ้ามีอยู่แล้ว ให้อัปเดตค่าที่ต้องการ (เช่น description, picture)
                existing_fruit.picture = validated_data.picture
                existing_fruit.description = validated_data.description
                session.add(existing_fruit) # เพิ่มเข้า session เพื่อให้ commit เปลี่ยนแปลง
                print(f"   Updated Fruit: {existing_fruit.name}")
            else:
                # ถ้ายังไม่มี ให้สร้างใหม่แล้วเพิ่ม
                new_fruit = Fruit(**validated_data.model_dump())
                session.add(new_fruit)
                print(f"   Inserted Fruit: {new_fruit.name}")

        # --- Insert/Update Vegetables ---
        for veg_data in Data_Vegetables:
            # 1. ค้นหาว่ามี Vegetable นี้อยู่แล้วหรือไม่
            existing_veg = session.exec(
                select(Vegetable).where(Vegetable.name == veg_data["name"])
            ).first()

            # 2. ใช้ Pydantic Schema เป็นตัวกรอง
            validated_data = VegetableInput(**veg_data)

            if existing_veg:
                # ถ้ามีอยู่แล้ว ให้อัปเดตค่าที่ต้องการ
                existing_veg.picture = validated_data.picture
                existing_veg.description = validated_data.description
                session.add(existing_veg) # เพิ่มเข้า session เพื่อให้ commit เปลี่ยนแปลง
                print(f"   Updated Vegetable: {existing_veg.name}")
            else:
                # ถ้ายังไม่มี ให้สร้างใหม่แล้วเพิ่ม
                new_veg = Vegetable(**validated_data.model_dump())
                session.add(new_veg)
                print(f"   Inserted Vegetable: {new_veg.name}")

        try:
            session.commit()
            print("\nData Insertion/Update Complete and COMMITTED successfully!")
        except Exception as e:
            session.rollback()
            print(f"\nERROR: Failed to commit data to database: {e}")
            print("Database changes have been rolled back.")

if __name__ == "__main__":
    insert_data()
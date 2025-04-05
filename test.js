const {WebUntis} = require("webuntis")
require("dotenv").config()
const fs = require("fs")
async function test(params) {
   let untis = new WebUntis(
        process.env.UNTIS_SCHOOL,
        process.env.UNTIS_USERNAME,
        process.env.UNTIS_PASSWORD,
        process.env.UNTIS_URL
    );
    await untis.login();

    let today = new Date();
    const end = new Date();
    end.setDate(today.getDate()+5)
    today.setDate(today.getDate()-100)
    let result = await untis.getAbsentLesson(today,end)

    //fs.writeFileSync("./data.json", JSON.stringify(result))    
    
    console.log(result)
    await untis.logout();
}

test()

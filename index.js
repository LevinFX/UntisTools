const getAbsentLessons = require('./util/getAbsentLessons');
const getClasses = require('./util/getClasses');
const getTimetable = require('./util/getTimetable');
const { logoutUntis } = require('./util/untisHelper');
const express = require("express");

const app = express();

app.get("/api/classes", async (req, res) => {
    try {
        const classes = await getClasses()
        res.send(classes)
    } catch (error) {
        res.send("Error occured")
        console.error("Error in classes Route:"+error)
    }finally {
        await logoutUntis()
    }
})

app.get("/api/absent", async (req, res) => {
    try {
        const absentLessons = await getAbsentLessons();
        res.send(absentLessons)
    } catch (error) {
        res.send("Error occured")
        console.error("Error in absent Route:"+error)
    }finally {
        await logoutUntis()
    }
})

app.listen(5000, () => {console.log("Server running on http://127.0.0.1:5000")})
/*async function main() {
    try {
        const classes = await getTimetable(); 
        console.log('Ergebnis:', classes);
    } catch (error) {
        console.error('Hauptfehler:', error);
    } finally {
        await logoutUntis();
    }
}

main();*/
const getAbsentLessons = require('./util/getAbsentLessons');

const getClasses = require('./util/getClasses');
const getData = require('./util/getData');
const getMotd = require('./util/getMotd');
const getStudents = require('./util/getStudents');
const getTeachers = require('./util/getTeachers');
const getTimetable = require('./util/getTimetable');
const { logoutUntis } = require('./util/untisHelper');

const express = require("express");
const fs = require('fs');

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

app.get("/api/timetable", async (req, res) => {
    try {
        const timetable = await getTimetable();
        res.send(timetable)
    } catch (error) {
        res.send("Error occured")
        console.error("Error in timetable Route:"+error)
    }finally {
        await logoutUntis()
    }
})

app.get("/api/data", async (req, res) => {
    try {
        const data = await getData();
        res.send(data)
        fs.writeFileSync("./data.json", JSON.stringify(data))

        var today = new Date();
        if(today.getDay() == 0 && data !== fs.readFileSync("./data-lastweek.json")) {
            fs.copyFileSync("./data.json", "./data-lastweek.json")
        }
    } catch (error) {
        res.send("Error occured")
        console.error("Error in data Route:"+error)
    }finally {
        await logoutUntis()
    }
})

app.get("/api/students", async (req, res) => {
    try {
        const students = await getStudents();
        res.send(students)
    } catch (error) {
        res.send("Error occured")
        console.error("Error in student Route:"+error)
    }finally {
        await logoutUntis()
    }
})

app.get("/api/motd", async (req, res) => {
    try {
        const motd = await getMotd();
        res.send(motd)
    } catch (error) {
        res.send("Error occured")
        console.error("Error in motd Route:"+error)
    }finally {
        await logoutUntis()
    }
})

app.get("/api/teachers", async (req, res) => {
    try {
        const teachers = await getTeachers();
        res.send(teachers)
    } catch (error) {
        res.send("Error occured")
        console.error("Error in teachers Route:"+error)
    }finally {
        await logoutUntis()
    }
})

app.listen(5000, () => {console.log("Server running on http://127.0.0.1:5000")})
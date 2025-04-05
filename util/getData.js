const { getAuthenticatedUntis } = require("./untisHelper");
const fs = require('fs')

module.exports = async function getData() {
  try {
    let today = new Date();
    let date = new Date().setDate(today.getTime() - 7);
    const untis = await getAuthenticatedUntis();
    const timetable = await untis.getOwnTimetableForWeek(today);

    
    // Zähler für aktuelle Woche initialisieren
    const counts = {
      ausfall: 0,
      vertretung: 0,
      arbeiten: 0,
      hausaufgaben: 0,
    };

    // Aktuelle Daten analysieren
    timetable.forEach((lesson) => {
      // Ausfall (CANCEL)
      if (lesson.cellState === "CANCEL") {
        counts.ausfall++;
      }

      // Vertretung (SUBSTITUTION)
      if (lesson.cellState === "SUBSTITUTION") {
        counts.vertretung++;
      }

      // Arbeiten (EXAM)
      if (lesson.cellState === "EXAM") {
        counts.arbeiten++;
      }

      // Hausaufgaben (Aufgabe in Texten)
      const hasHomework = [
        lesson.substText,
        lesson.periodText,
        lesson.periodInfo,
      ].some((text) => text && text.includes("Aufgabe"));
      if (hasHomework) {
        counts.hausaufgaben++;
      }
    });

    
    let lastWeekCounts = fs.readFileSync("./data-lastweek.json")

    // Differenzen berechnen
    return [
      {
        type: "Ausfall",
        current: counts.ausfall,
        difference: counts.ausfall - (lastWeekCounts?.ausfall || 0),
      },
      {
        type: "Vertretung",
        current: counts.vertretung,
        difference: counts.vertretung - (lastWeekCounts?.vertretung || 0),
      },
      {
        type: "Arbeiten",
        current: counts.arbeiten,
        difference: counts.arbeiten - (lastWeekCounts?.arbeiten || 0),
      },
      {
        type: "Hausaufgaben",
        current: counts.hausaufgaben,
        difference: counts.hausaufgaben - (lastWeekCounts?.hausaufgaben || 0),
      },
    ];
  } catch (error) {
    console.error("Fehler in getData:", error);
    throw error;
  }
};

const { getAuthenticatedUntis } = require('./untisHelper');

module.exports = async function getStudents() {
    try {
        const untis = await getAuthenticatedUntis();
        let today = new Date()
        const MOTD = await untis.getNewsWidget(today)

        return MOTD;
    } catch (error) {
        console.error('Fehler in getMOTD:', error);
        throw error;
    }
};
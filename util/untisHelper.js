const { WebUntis } = require('webuntis');
require('dotenv').config();

let untisInstance = null;

module.exports = {
    getAuthenticatedUntis: async () => {
        if (!untisInstance) {
            untisInstance = new WebUntis(
                process.env.UNTIS_SCHOOL,
                process.env.UNTIS_USERNAME,
                process.env.UNTIS_PASSWORD,
                process.env.UNTIS_URL
            );
            await untisInstance.login();
        }
        return untisInstance;
    },
    logoutUntis: async () => {
        if (untisInstance) {
            await untisInstance.logout();
            untisInstance = null;
        }
    }
};
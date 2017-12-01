/**
 * Log 
 */

function log() {
    try {
        /** metodo comum de todos browser */
        console.log.apply(console, arguments);
    } catch (e) {
        /**
         * Catch qualquer falha no logging
         */
        try {
            /** Tentar log via opera */
            opera.posError.apply(opera, arguments);
        } catch (e) {
            /** Em caso de falha usar metodo alert() como ultima instancia */

            alert(Array.prototype.join.call(arguments, " "));
        }
    }
}
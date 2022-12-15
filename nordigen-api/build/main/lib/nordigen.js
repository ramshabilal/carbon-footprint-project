"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const node_fetch_1 = __importDefault(require("node-fetch"));
/**
 * Unofficial Nordigen API for JavaScript
 *
 * @author vantezzen (https://github.com/vantezzen)
 * @license MIT License
 */
class Nordigen {
    /**
     * Create a new instance of the Nordigen API
     *
     * ### Example (es module)
     * ```js
     * import Nordigen from 'nordigen'
     * const nordigen = new Nordigen();
     * ```
     *
     * @param accessToken Access Token for the Nordigen API
     * @param endpoint Endpoint URL for the Nordigen API
     */
    constructor(accessToken, endpoint = 'https://ob.nordigen.com/api') {
        this.accessToken = accessToken;
        this.endpoint = endpoint;
    }
    /**
     * Make an authenticated request to the Nordigen API
     *
     * @param path Relative path to the requested endpoint
     * @param method Method to use
     * @param body Message Body
     * @returns JSON Response
     */
    async makeRequest(path, method = 'GET', body = false) {
        const request = await node_fetch_1.default(`${this.endpoint}${path}`, Object.assign({ method, headers: {
                accept: 'application/json',
                Authorization: `Token ${this.accessToken}`,
                'Content-Type': 'application/json',
            } }, (body ? { body: JSON.stringify(body) } : {})));
        const response = await request.json();
        return response;
    }
    /**
     * Get a list of ASPSPs (Banks) for a given country
     *
     * @param countryCode Country code to use, e.g. "gb" for Great Britain
     * @returns Array of ASPSPs
     */
    async getASPSPsForCountry(countryCode) {
        return await this.makeRequest(`/aspsps/?country=${countryCode}`);
    }
    /**
     * Create a new end user agreement for a user.
     * Use this step only if you want to specify the length of transaction history you want to retrieve.
     * If you skip this step, by default 90 days of transaction history will be retrieved
     *
     * @param enduser_id A unique end-user ID of someone who's using your services, it has to be unique within your solution. Usually, it's UUID;
     * @param aspsp_id ASPSP ID (Bank ID) to use
     * @param max_historical_days The length of the transaction history to be retrieved
     * @returns End user agreement
     */
    async createEndUserAgreement(enduser_id, aspsp_id, max_historical_days = 90) {
        const response = await this.makeRequest('/agreements/enduser/', 'POST', {
            enduser_id,
            aspsp_id,
            max_historical_days,
        });
        if (response.created) {
            response.created = new Date(response.created);
        }
        if (response.accepted) {
            response.accepted = new Date(response.accepted);
        }
        return response;
    }
    /**
     * Create a requisition for a user
     *
     * @param enduser_id A unique end-user ID of someone who's using your services, it has to be unique within your solution. Usually, it's a UUID. If you have an end user agreement it has to be the ID of that user
     * @param redirect URI where the end user will be redirected after finishing authentication in ASPSP
     * @param reference Additional layer of unique ID defined by you
     * @param agreements As an array of end user agreement IDs or an empty array if you don't have one
     * @param user_language To enforce a language for all end user steps hosted by Nordigen passed as a two-letter country code (ISO 3166). If user_language is not defined a language set in browser will be used to determine language
     * @returns Requisition answer
     */
    async createRequisition(enduser_id, redirect, reference, agreements = [], user_language = undefined) {
        return await this.makeRequest('/requisitions/', 'POST', {
            enduser_id,
            redirect,
            reference,
            agreements,
            user_language,
        });
    }
    /**
     * Get the link for the user requisition
     *
     * @param requsition Requisition as returned by `createRequisition`
     * @param aspsp_id ID for the user's ASPSP (Bank)
     * @returns Link for "false" if Nordigen didn't return one
     */
    async getRequisitionLink(requsition, aspsp_id) {
        const response = await this.makeRequest(`/requisitions/${requsition.id}/links/`, 'POST', {
            aspsp_id,
        });
        if (response && response.initiate) {
            return response.initiate;
        }
        return false;
    }
    /**
     * Get information about a user requisition.
     * This can be used to get a list of all user accounts by getting requisition.accounts
     *
     * @param requisition_id Requisition ID of an existing requistion
     * @returns Requisition info
     */
    async getRequisitionInfo(requisition_id) {
        return await this.makeRequest(`/requisitions/${requisition_id}/`);
    }
    /**
     * Get a list of all balances an account ID holds
     *
     * @param account_id Account ID to check
     * @returns Balances for the account
     */
    async getAccountBalances(account_id) {
        return await this.makeRequest(`/accounts/${account_id}/balances/`);
    }
    /**
     * Get a list of all transactions an account ID holds
     *
     * @param account_id Account ID to check
     * @returns Transactions for the account
     */
    async getAccountTransactions(account_id) {
        return await this.makeRequest(`/accounts/${account_id}/transactions/`);
    }
    /**
     * Get account details for an account
     *
     * @param account_id Account ID to check
     * @returns Details for the account
     */
    async getAccountDetails(account_id) {
        return await this.makeRequest(`/accounts/${account_id}/details/`);
    }
}
exports.default = Nordigen;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoibm9yZGlnZW4uanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi8uLi8uLi9zcmMvbGliL25vcmRpZ2VuLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7O0FBQUEsNERBQStCO0FBVy9COzs7OztHQUtHO0FBQ0gsTUFBcUIsUUFBUTtJQVczQjs7Ozs7Ozs7Ozs7T0FXRztJQUNILFlBQVksV0FBbUIsRUFBRSxRQUFRLEdBQUcsNkJBQTZCO1FBQ3ZFLElBQUksQ0FBQyxXQUFXLEdBQUcsV0FBVyxDQUFDO1FBQy9CLElBQUksQ0FBQyxRQUFRLEdBQUcsUUFBUSxDQUFDO0lBQzNCLENBQUM7SUFFRDs7Ozs7OztPQU9HO0lBQ0gsS0FBSyxDQUFDLFdBQVcsQ0FDZixJQUFZLEVBQ1osTUFBTSxHQUFHLEtBQUssRUFDZCxPQUF3QyxLQUFLO1FBRTdDLE1BQU0sT0FBTyxHQUFHLE1BQU0sb0JBQUssQ0FBQyxHQUFHLElBQUksQ0FBQyxRQUFRLEdBQUcsSUFBSSxFQUFFLGtCQUNuRCxNQUFNLEVBQ04sT0FBTyxFQUFFO2dCQUNQLE1BQU0sRUFBRSxrQkFBa0I7Z0JBQzFCLGFBQWEsRUFBRSxTQUFTLElBQUksQ0FBQyxXQUFXLEVBQUU7Z0JBQzFDLGNBQWMsRUFBRSxrQkFBa0I7YUFDbkMsSUFDRSxDQUFDLElBQUksQ0FBQyxDQUFDLENBQUMsRUFBRSxJQUFJLEVBQUUsSUFBSSxDQUFDLFNBQVMsQ0FBQyxJQUFJLENBQUMsRUFBRSxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUMsRUFDL0MsQ0FBQztRQUNILE1BQU0sUUFBUSxHQUFHLE1BQU0sT0FBTyxDQUFDLElBQUksRUFBRSxDQUFDO1FBQ3RDLE9BQU8sUUFBUSxDQUFDO0lBQ2xCLENBQUM7SUFFRDs7Ozs7T0FLRztJQUNILEtBQUssQ0FBQyxtQkFBbUIsQ0FBQyxXQUFtQjtRQUMzQyxPQUFPLE1BQU0sSUFBSSxDQUFDLFdBQVcsQ0FBQyxvQkFBb0IsV0FBVyxFQUFFLENBQUMsQ0FBQztJQUNuRSxDQUFDO0lBRUQ7Ozs7Ozs7OztPQVNHO0lBQ0gsS0FBSyxDQUFDLHNCQUFzQixDQUMxQixVQUFrQixFQUNsQixRQUFnQixFQUNoQixtQkFBbUIsR0FBRyxFQUFFO1FBRXhCLE1BQU0sUUFBUSxHQUFHLE1BQU0sSUFBSSxDQUFDLFdBQVcsQ0FBQyxzQkFBc0IsRUFBRSxNQUFNLEVBQUU7WUFDdEUsVUFBVTtZQUNWLFFBQVE7WUFDUixtQkFBbUI7U0FDcEIsQ0FBQyxDQUFDO1FBRUgsSUFBSSxRQUFRLENBQUMsT0FBTyxFQUFFO1lBQ3BCLFFBQVEsQ0FBQyxPQUFPLEdBQUcsSUFBSSxJQUFJLENBQUMsUUFBUSxDQUFDLE9BQU8sQ0FBQyxDQUFDO1NBQy9DO1FBQ0QsSUFBSSxRQUFRLENBQUMsUUFBUSxFQUFFO1lBQ3JCLFFBQVEsQ0FBQyxRQUFRLEdBQUcsSUFBSSxJQUFJLENBQUMsUUFBUSxDQUFDLFFBQVEsQ0FBQyxDQUFDO1NBQ2pEO1FBRUQsT0FBTyxRQUFRLENBQUM7SUFDbEIsQ0FBQztJQUVEOzs7Ozs7Ozs7T0FTRztJQUNILEtBQUssQ0FBQyxpQkFBaUIsQ0FDckIsVUFBa0IsRUFDbEIsUUFBZ0IsRUFDaEIsU0FBaUIsRUFDakIsYUFBMEMsRUFBRSxFQUM1QyxnQkFBb0MsU0FBUztRQUU3QyxPQUFPLE1BQU0sSUFBSSxDQUFDLFdBQVcsQ0FBQyxnQkFBZ0IsRUFBRSxNQUFNLEVBQUU7WUFDdEQsVUFBVTtZQUNWLFFBQVE7WUFDUixTQUFTO1lBQ1QsVUFBVTtZQUNWLGFBQWE7U0FDZCxDQUFDLENBQUM7SUFDTCxDQUFDO0lBRUQ7Ozs7OztPQU1HO0lBQ0gsS0FBSyxDQUFDLGtCQUFrQixDQUN0QixVQUF1QixFQUN2QixRQUFnQjtRQUVoQixNQUFNLFFBQVEsR0FBRyxNQUFNLElBQUksQ0FBQyxXQUFXLENBQ3JDLGlCQUFpQixVQUFVLENBQUMsRUFBRSxTQUFTLEVBQ3ZDLE1BQU0sRUFDTjtZQUNFLFFBQVE7U0FDVCxDQUNGLENBQUM7UUFDRixJQUFJLFFBQVEsSUFBSSxRQUFRLENBQUMsUUFBUSxFQUFFO1lBQ2pDLE9BQU8sUUFBUSxDQUFDLFFBQVEsQ0FBQztTQUMxQjtRQUNELE9BQU8sS0FBSyxDQUFDO0lBQ2YsQ0FBQztJQUVEOzs7Ozs7T0FNRztJQUNILEtBQUssQ0FBQyxrQkFBa0IsQ0FBQyxjQUFzQjtRQUM3QyxPQUFPLE1BQU0sSUFBSSxDQUFDLFdBQVcsQ0FBQyxpQkFBaUIsY0FBYyxHQUFHLENBQUMsQ0FBQztJQUNwRSxDQUFDO0lBRUQ7Ozs7O09BS0c7SUFDSCxLQUFLLENBQUMsa0JBQWtCLENBQUMsVUFBa0I7UUFDekMsT0FBTyxNQUFNLElBQUksQ0FBQyxXQUFXLENBQUMsYUFBYSxVQUFVLFlBQVksQ0FBQyxDQUFDO0lBQ3JFLENBQUM7SUFFRDs7Ozs7T0FLRztJQUNILEtBQUssQ0FBQyxzQkFBc0IsQ0FBQyxVQUFrQjtRQUM3QyxPQUFPLE1BQU0sSUFBSSxDQUFDLFdBQVcsQ0FBQyxhQUFhLFVBQVUsZ0JBQWdCLENBQUMsQ0FBQztJQUN6RSxDQUFDO0lBRUQ7Ozs7O09BS0c7SUFDSCxLQUFLLENBQUMsaUJBQWlCLENBQUMsVUFBa0I7UUFDeEMsT0FBTyxNQUFNLElBQUksQ0FBQyxXQUFXLENBQUMsYUFBYSxVQUFVLFdBQVcsQ0FBQyxDQUFDO0lBQ3BFLENBQUM7Q0FDRjtBQXpMRCwyQkF5TEMifQ==
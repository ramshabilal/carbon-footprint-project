import { AccountDetailData, ASPSP, BalanceData, EndUserAgreement, Requisition, TransactionData } from './types';
/**
 * Unofficial Nordigen API for JavaScript
 *
 * @author vantezzen (https://github.com/vantezzen)
 * @license MIT License
 */
export default class Nordigen {
    /**
     * Access Token for the Nordigen API
     */
    private readonly accessToken;
    /**
     * Endpoint URL to use
     */
    readonly endpoint: string;
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
    constructor(accessToken: string, endpoint?: string);
    /**
     * Make an authenticated request to the Nordigen API
     *
     * @param path Relative path to the requested endpoint
     * @param method Method to use
     * @param body Message Body
     * @returns JSON Response
     */
    makeRequest(path: string, method?: string, body?: Record<string, unknown> | false): Promise<any>;
    /**
     * Get a list of ASPSPs (Banks) for a given country
     *
     * @param countryCode Country code to use, e.g. "gb" for Great Britain
     * @returns Array of ASPSPs
     */
    getASPSPsForCountry(countryCode: string): Promise<readonly ASPSP[]>;
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
    createEndUserAgreement(enduser_id: string, aspsp_id: string, max_historical_days?: number): Promise<EndUserAgreement>;
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
    createRequisition(enduser_id: string, redirect: string, reference: string, agreements?: readonly EndUserAgreement[], user_language?: string | undefined): Promise<Requisition>;
    /**
     * Get the link for the user requisition
     *
     * @param requsition Requisition as returned by `createRequisition`
     * @param aspsp_id ID for the user's ASPSP (Bank)
     * @returns Link for "false" if Nordigen didn't return one
     */
    getRequisitionLink(requsition: Requisition, aspsp_id: string): Promise<string | false>;
    /**
     * Get information about a user requisition.
     * This can be used to get a list of all user accounts by getting requisition.accounts
     *
     * @param requisition_id Requisition ID of an existing requistion
     * @returns Requisition info
     */
    getRequisitionInfo(requisition_id: string): Promise<Requisition>;
    /**
     * Get a list of all balances an account ID holds
     *
     * @param account_id Account ID to check
     * @returns Balances for the account
     */
    getAccountBalances(account_id: string): Promise<BalanceData>;
    /**
     * Get a list of all transactions an account ID holds
     *
     * @param account_id Account ID to check
     * @returns Transactions for the account
     */
    getAccountTransactions(account_id: string): Promise<TransactionData>;
    /**
     * Get account details for an account
     *
     * @param account_id Account ID to check
     * @returns Details for the account
     */
    getAccountDetails(account_id: string): Promise<AccountDetailData>;
}

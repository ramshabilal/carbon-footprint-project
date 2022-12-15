/**
 * A Nordigen ASPSP (Bank)
 */
export declare type ASPSP = {
    readonly id: string;
    readonly name: string;
    readonly bic: string;
    readonly countries: readonly string[];
};
/**
 * A bank account in any bank
 * Please note that you might only get the account IBAN without any further information
 */
export declare type BankAccount = {
    readonly iban: string;
    readonly resourceId?: string;
    readonly currency?: string;
    readonly ownerName?: string;
    readonly product?: string;
    readonly cashAccountType?: string;
    readonly name?: string;
};
/**
 * An End User Agreement
 */
export declare type EndUserAgreement = {
    readonly id: string;
    readonly created: Date;
    readonly accepted: Date | null;
    readonly max_historical_days: number;
    readonly access_valid_for_days: number;
    readonly enduser_id: string;
    readonly aspsp_id: string;
};
/**
 * Nordigen Requisition
 */
export declare type Requisition = {
    readonly id: string;
    readonly redirect: string;
    readonly status: string;
    readonly agreements: readonly string[];
    readonly accounts: readonly string[];
    readonly reference: string;
    readonly enduser_id: string;
    readonly user_language: string;
};
export declare type AmountValue = {
    readonly currency: string;
    readonly amount: string;
};
/**
 * A single account balance
 */
export declare type Balance = {
    readonly balanceAmount: AmountValue;
    readonly balanceType: 'closingBooked' | 'expected';
    readonly referenceDate: string;
};
/**
 * Balance data from the Nordigen API
 */
export declare type BalanceData = {
    readonly account?: BankAccount;
    readonly balances: readonly Balance[];
};
/**
 * A single transaction on the account
 */
export declare type Transaction = {
    readonly transactionId: string;
    readonly creditorName?: string;
    readonly creditorAccount?: BankAccount;
    readonly debtorName?: string;
    readonly debtorAccount?: BankAccount;
    readonly transactionAmount: AmountValue;
    readonly bookingDate: string;
    readonly valueDate: string;
    readonly remittanceInformationUnstructured: string;
};
/**
 * Data returned by the transaction endpoint
 */
export declare type TransactionData = {
    readonly account?: BankAccount;
    readonly balances: readonly Balance[];
    readonly transactions: {
        readonly booked: readonly Transaction[];
        readonly pending: readonly Transaction[];
    };
};
/**
 * Data returned by the account detail endpoint
 * You will most likely get all information available in the "BankAccount" type here
 */
export declare type AccountDetailData = {
    readonly account: BankAccount;
};

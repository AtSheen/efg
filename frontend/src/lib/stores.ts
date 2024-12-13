import { writable, type Writable } from 'svelte/store';

export const companyCode: Writable<string> = writable('');
export const vendorNumber: Writable<string> = writable('');
export const rowsLen: Writable<number> = writable(0)
export const rowsLen2: Writable<number> = writable(0)
export const rowsLen3: Writable<number> = writable(0);

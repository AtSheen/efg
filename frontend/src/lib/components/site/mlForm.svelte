<script lang="ts">
	import Combobox from '$lib/components/site/combobox.svelte';
	import { Input } from '$lib/components/ui/input';
	import { writable } from 'svelte/store';
	import { ScrollArea } from '$lib/components/ui/scroll-area/index.js';

	import { Button } from '$lib/components/ui/button';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import { Label } from '$lib/components/ui/label';
	import * as Select from '$lib/components/ui/select';

	import Factory from 'lucide-svelte/icons/factory';
	import Hash from 'lucide-svelte/icons/hash';
	import Loader2 from 'lucide-svelte/icons/loader-circle';
	import { companyCode } from '$lib/stores';
	import * as Card from '$lib/components/ui/card';
	import Table from './table.svelte';
	import { dev } from '$app/environment';
	import Barchart from './barchart.svelte';

	const comboboxOpts = [
		{ label: '0', value: '0' },
		{ label: '5', value: '5' },
		{ label: '6', value: '6' },
		{ label: '12', value: '12' },
		{ label: '14', value: '14' },
		{ label: '15', value: '15' },
		{ label: '20', value: '20' },
		{ label: '24', value: '24' },
		{ label: '25', value: '25' },
		{ label: 'Foreign VAT Rate', value: 'foreignVatRate' }
	];

	let inputs = [
		{ label: 'PID Number', id: 'PIDNumber', value: '', icon: Hash },
		{ label: 'Company Code', id: 'companyCode', value: '', icon: Factory },
		{ label: 'Vendor Number', id: 'vendorNumber', value: '', icon: Factory }
	];

	let isReverseCharge: boolean = true;
	let isGoods: boolean = true;
	let isServices: boolean = false;

	let apAr: {
		label: string;
		value: string;
	}[] = [
		{ label: 'AP', value: 'AP' },
		{ label: 'AR', value: 'AR' }
	];

	let vatRate = '0';
	let apArSelected = apAr[0];

	let buttonDisabled = false;

	$: {
		buttonDisabled = !(inputs.every((input) => input.value) && vatRate);
	}

	$: {
		$companyCode = inputs[1].value;
	}

	// Function to check if an input is empty
	function isInputEmpty(value: string) {
		return !value || value.trim() === '';
	}

	let loadingPrediction = writable(false);
	let data1 = writable(null);

	async function handleSubmit(event: any) {
		event.preventDefault();
		loadingPrediction.set(true);

		const taxCodePredictionBody = {
			pID: inputs[0].value,
			companyCode: inputs[1].value,
			vendorNumber: inputs[2].value,
			vatRate: vatRate,
			isReverseCharge: isReverseCharge,
			goods: isGoods,
			services: isServices,
			apAr: apArSelected.value
		};

		const url = dev ? 'http://127.0.0.1:8080/get_tax_code_prediction' : 'get_tax_code_prediction';

		const fetchTaxCodePrediction = fetch(url, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(taxCodePredictionBody)
		})
			.then(async (response) => {
				if (response.ok) {
					let result = await response.json();
					result.filtered_tax_codes = result.filtered_tax_codes;
					data1.set(result);
					console.log('Tax Code Prediction:', result);
				} else {
					throw new Error('Failed to fetch tax code prediction');
				}
			})
			.catch((error) => console.error('Error fetching tax code prediction:', error))
			.finally(() => loadingPrediction.set(false));
		await fetchTaxCodePrediction;
	}
</script>

<div class="flex h-[88vh] flex-col gap-8">
	<div class="border bg-white p-4 shadow-sm">
		<form class="flex flex-col gap-4" on:submit={handleSubmit}>
			<div class="flex flex-wrap items-center justify-between gap-4">
				{#each inputs as input (input.id)}
					<div class="flex flex-grow flex-col gap-3">
						<Label for={input.id}><b>{input.label}*</b></Label>
						<div class="relative">
							<Input
								type="text"
								id={input.id}
								placeholder={input.label}
								required
								name={input.id}
								bind:value={input.value}
								class="border-2 border-gray-400 pl-10  {isInputEmpty(input.value)
									? 'bg-red-100'
									: ''}"
							/>
							<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
								<svelte:component this={input.icon} class="h-5 w-5 text-gray-400" />
							</div>
						</div>
					</div>
				{/each}
			</div>
			<div class="grid w-full grid-cols-2 gap-4">
				<div class="w-full">
					<Combobox data={comboboxOpts} placeholder="Vat Rate (%)*" bind:value={vatRate} />
					<input type="hidden" name="vatRate" bind:value={vatRate} />
				</div>
				<div class="w-full">
					<Select.Root
						selected={apArSelected}
						onSelectedChange={(value) => {
							if (value?.label && value.value) {
								apArSelected = {
									label: value?.label,
									value: value?.value
								};
							}
						}}
					>
						<div class="flex flex-col gap-3">
							<Label><b>AP/AR:</b></Label>
							<Select.Trigger class="h-9 w-full">
								<Select.Value placeholder="AP/AR" />
							</Select.Trigger>
						</div>
						<Select.Content>
							{#each apAr as apArItem (apArItem.value)}
								<Select.Item value={apArItem.value}>{apArItem.label}</Select.Item>
							{/each}
						</Select.Content>
						<input hidden bind:value={apArSelected.value} name="apAr" />
					</Select.Root>
				</div>
			</div>
			<div class="flex items-center gap-4">
				<!-- First Checkbox (50% width) -->
				<div class="flex w-1/2 items-center space-x-2">
					<Label
						for="isReverseCharged"
						class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
					>
						<b>Reverse Charge:</b>
					</Label>
					<input name="isReverseCharged" value={isReverseCharge} hidden required />
					<Checkbox id="isReverseCharged" bind:checked={isReverseCharge} />
				</div>

				<!-- Second Checkbox (25% width) -->
				<div class="flex w-1/4 items-center space-x-2">
					<Label
						for="isGoods"
						class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
					>
						<b>Goods:</b>
					</Label>
					<input name="isGoods" value={isGoods} hidden required />
					<Checkbox id="isGoods" bind:checked={isGoods} />
				</div>

				<!-- Third Checkbox (25% width) -->
				<div class="flex w-1/4 items-center space-x-2">
					<Label
						for="isServices"
						class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
					>
						<b>Services:</b>
					</Label>
					<input name="isServices" value={isServices} hidden required />
					<Checkbox id="isServices" bind:checked={isServices} />
				</div>
			</div>

			<div class="flex items-center justify-end">
				<Button
					type="submit"
					disabled={buttonDisabled}
					class="w-1/2 bg-emerald-400 text-black hover:bg-emerald-500">Submit</Button
				>
			</div>
		</form>
	</div>
	<ScrollArea class="flex h-full flex-col justify-between p-2">
		{#if $loadingPrediction}
			<div class="flex h-full items-center justify-center">
				<Loader2 class="size-32 animate-spin text-zinc-300" />
			</div>
		{:else if $data1}
			<div class=" flex flex-col gap-2">
				<p>Company Name: <span class="font-bold">{$data1.reportingName}</span></p>
				<p>Vendor Name: <span class="font-bold">{$data1.vendorName}</span></p>
			</div>
			<div class="flex h-full flex-col justify-between gap-4">
				<div class="mt-6 flex items-center justify-between">
					<Card.Root class="w-1/2">
						<Card.Content class="p-6">
							<div class="flex flex-col items-center">
								<h1 class="text-5xl font-bold">{$data1.predictedTaxCode}</h1>
								<div class="flex flex-col -space-y-1">
									<p class="text-lg">
										confidence: <span class="font-semibold">{$data1.confidenceScore}</span>
									</p>
									<p class="text-lg font-normal">Predicted Tax Code</p>
								</div>
							</div>
						</Card.Content>
					</Card.Root>
					<div class="-mt-8 min-w-[45%]">
						<Barchart
							xKey="Tax Code"
							yKey="prob"
							xLabel="Tax Code"
							yLabel="Probability"
							data={$data1.taxCodePredictionProbabilities}
						/>
					</div>
				</div>
				<div class="w-full bg-white">
					<Table data={$data1.filtered_tax_codes} />
				</div>
			</div>
		{/if}
	</ScrollArea>
</div>

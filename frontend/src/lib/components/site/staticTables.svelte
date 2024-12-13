<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import * as Tabs from '$lib/components/ui/tabs';
	import DynamicDataTable from './datatable/dynamic-datatable.svelte';
	import { dev } from '$app/environment';
	import { Loader2Icon } from 'lucide-svelte';

	const data1 = writable(null);
	const data2 = writable(null);
	const data3 = writable(null);

	async function fetchData(url: RequestInfo | URL) {
		try {
			const response = await fetch(url);
			if (response.ok) {
				return await response.json();
			} else {
				console.error('Error fetching data from', url);
				return null;
			}
		} catch (error) {
			console.error('Error fetching data from', url, error);
			return null;
		}
	}

	onMount(() => {
		const devUrl = 'http://127.0.0.1:8080';

		Promise.all([
			fetchData(
				`${dev ? `${devUrl + '/get_attention_list_table'}` : '/get_attention_list_table'}`
			).then((result) => data1.set(result)),
			fetchData(`${dev ? `${devUrl + '/get_vat_ip_table'}` : '/get_vat_ip_table'}`).then((result) =>
				data2.set(result)
			),
			fetchData(
				`${dev ? `${devUrl + '/get_historical_meta_table'}` : '/get_historical_meta_table'}`
			).then((result) => data3.set(result))
		]);
	});

	type Column = {
		header: string;
		accessor: string;
		sortable: boolean;
		filterable?: boolean;
	};

	function generateColumns(data: any[]): Column[] {
		if (!data.length) return [];
		const firstRow = data[0];
		return Object.keys(firstRow).map((key) => ({
			header: key.charAt(0).toUpperCase() + key.slice(1),
			accessor: key,
			sortable: true,
			filterable: true
		}));
	}

	$: attentionListColumns = generateColumns($data1?.['attentionList'] || []);
	$: ipVatListColumns = generateColumns($data2?.['ipVatList'] || []);
	$: historicalMetaColumns = generateColumns($data3?.['historicalMeta'] || []);

	let tab1Rows: number;
	let tab2Rows: number;
	let tab3Rows: number;
</script>

{#if $data1 && $data2 && $data3}
	<Tabs.Root value="attentionList" class="w-full mt-2">
		<Tabs.List class="w-fit p-0">
			<Tabs.Trigger value="attentionList" class="relative"
				>Attention List
				<p class="absolute left-1 -top-3 rounded-[7px] text-white p-1 py-0 text-xs bg-red-500">{tab1Rows}</p>
			</Tabs.Trigger>
			<Tabs.Trigger value="ipVatList" class="relative"
				>VAT IP List
				<p class="absolute -left-1 -top-3 rounded-[7px] text-white p-1 py-0 text-xs bg-red-500">{tab2Rows}</p>
			</Tabs.Trigger>
			<Tabs.Trigger value="historicalMeta" class="relative"
				>Historical Meta
				<p class="absolute -left-1 -top-3 rounded-[7px] text-white p-1 py-0 text-xs bg-red-500">{tab3Rows}</p>
			</Tabs.Trigger>
		</Tabs.List>

		<Tabs.Content value="attentionList">
			{#if $data1?.['attentionList']?.length > 0}
				<DynamicDataTable
					data={$data1['attentionList']}
					columns={attentionListColumns}
					rowsPerPage={10}
					bind:rowsLen={tab1Rows}
				/>
			{:else}
				<p>No data available.</p>
			{/if}
		</Tabs.Content>

		<Tabs.Content value="ipVatList">
			{#if $data2?.['ipVatList']?.length > 0}
				<DynamicDataTable
					data={$data2['ipVatList']}
					columns={ipVatListColumns}
					rowsPerPage={10}
					bind:rowsLen={tab2Rows}
				/>
			{:else}
				<p>No data available.</p>
			{/if}
		</Tabs.Content>

		<Tabs.Content value="historicalMeta">
			{#if $data3?.['historicalMeta']?.length > 0}
				<DynamicDataTable
					data={$data3['historicalMeta']}
					columns={historicalMetaColumns}
					rowsPerPage={10}
					bind:rowsLen={tab3Rows}
				/>
			{:else}
				<p>No data available.</p>
			{/if}
		</Tabs.Content>
	</Tabs.Root>
{:else}
	<div class="flex h-full items-center justify-center">
		<Loader2Icon class="size-20 animate-spin" />
	</div>
{/if}

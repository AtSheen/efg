<script lang="ts">
	import { Render, Subscribe, createRender, createTable } from 'svelte-headless-table';
	import {
		addHiddenColumns,
		addPagination,
		addSelectedRows,
		addSortBy,
		addTableFilter
	} from 'svelte-headless-table/plugins';
	import { readable, type Readable, writable } from 'svelte/store';
	import ArrowUpDown from 'lucide-svelte/icons/arrow-up-down';
	import ChevronDown from 'lucide-svelte/icons/chevron-down';
	import * as Table from '$lib/components/ui/table';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import { cn } from '$lib/utils.js';
	import { Input } from '$lib/components/ui/input';
	import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from 'lucide-svelte';
	import * as Select from '$lib/components/ui/select';
	import { companyCode } from '$lib/stores';
	import Label from '$lib/components/ui/label/label.svelte';

	type ColumnDefinition<T> = {
		header: string;
		accessor: keyof T;
		cell?: (value: any) => string;
		sortable?: boolean;
		filterable?: boolean;
		hidden?: boolean;
	};

	type TableProps<T extends Record<string, any>> = {
		data: T[];
		columns: ColumnDefinition<T>[];
		rowsPerPage?: number;
		showPagination?: boolean;
		showFiltering?: boolean;
		showColumnToggle?: boolean;
	};

	export let data: TableProps<any>['data'];
	export let columns: TableProps<any>['columns'];
	export let rowsPerPage = 10;
	export let showPagination = true;
	export let showFiltering = true;
	export let showColumnToggle = true;

	const initialHiddenState = columns.reduce(
		(acc, col) => {
			acc[col.accessor as string] = col.hidden ?? false;
			return acc;
		},
		{} as Record<string, boolean>
	);

	const hiddenColumns = writable(initialHiddenState);

	const table = createTable(readable(data), {
		sort: addSortBy({ disableMultiSort: true }),
		page: addPagination({ initialPageSize: rowsPerPage }),
		filter: addTableFilter({
			fn: ({ filterValue, value }) =>
				String(value).toLowerCase().includes(String(filterValue).toLowerCase())
		}),
		select: addSelectedRows(),
		hide: addHiddenColumns()
	});

	$: tableColumns = table.createColumns(
		columns.map((col) =>
			table.column({
				header: col.header,
				accessor: col.accessor as string,
				cell: ({ value }) => (col.cell ? col.cell(value) : String(value)),
				plugins: {
					sort: { disable: !col.sortable },
					filter: { exclude: !col.filterable }
				}
			})
		)
	);

	$: ({ headerRows, pageRows, tableAttrs, tableBodyAttrs, flatColumns, pluginStates, rows } =
		table.createViewModel(tableColumns));

	$: ({ sortKeys } = pluginStates.sort);
	$: ({ hasNextPage, hasPreviousPage, pageIndex, pageCount, pageSize } = pluginStates.page);
	$: ({ filterValue } = pluginStates.filter);
	$: ({ selectedDataIds } = pluginStates.select);

	$: $hiddenColumns,
		pluginStates.hide.hiddenColumnIds.set(
			Object.entries($hiddenColumns)
				.filter(([, hidden]) => hidden)
				.map(([id]) => id)
		);

	function toggleColumnVisibility(columnId: string) {
		hiddenColumns.update((state) => ({
			...state,
			[columnId]: !state[columnId]
		}));
	}

	$: {
		if ($companyCode) {
			$filterValue = $companyCode;
		}
	}

	export let rowsLen: number = 0;

	$: {
		if ($rows && $rows.length) {
			rowsLen = $rows.length;
		}
	}
</script>

<div class="w-full p-1">
	{#if showFiltering}
		<div class="mb-4 flex items-center">
			<div class="flex flex-col gap-2">
				<Label for="input">Company Code</Label>
				<Input
					class="max-w-sm"
					placeholder="Filter..."
					type="text"
					bind:value={$filterValue}
					id="input"
				/>
			</div>
			{#if showColumnToggle}
				<DropdownMenu.Root>
					<DropdownMenu.Trigger asChild let:builder>
						<Button variant="outline" class="ml-auto" builders={[builder]}>
							Columns <ChevronDown class="ml-2 h-4 w-4" />
						</Button>
					</DropdownMenu.Trigger>
					<DropdownMenu.Content>
						{#each flatColumns as col}
							<DropdownMenu.CheckboxItem
								checked={!$hiddenColumns[col.id]}
								onCheckedChange={() => toggleColumnVisibility(col.id)}
							>
								{col.header}
							</DropdownMenu.CheckboxItem>
						{/each}
					</DropdownMenu.Content>
				</DropdownMenu.Root>
			{/if}
		</div>
	{/if}
	<div class="flex flex-col gap-4">
		<div class="rounded-md border">
			<Table.Root {...$tableAttrs} class="bg-white">
				<Table.Header>
					{#each $headerRows as headerRow}
						<Subscribe rowAttrs={headerRow.attrs()}>
							<Table.Row>
								{#each headerRow.cells as cell (cell.id)}
									<Subscribe attrs={cell.attrs()} let:attrs props={cell.props()} let:props>
										<Table.Head {...attrs} class={cn('p-1 [&:has([role=checkbox])]:pl-3')}>
											{#if columns.find((col) => col.accessor === cell.id)?.sortable}
												<Button
													variant="ghost"
													on:click={props.sort.toggle}
													class="flex items-center justify-between p-3 py-2"
												>
													<Render of={cell.render()} />
													<ArrowUpDown
														class={cn(
															$sortKeys[0]?.id === cell.id && 'text-foreground',
															'ml-2 h-4 w-4'
														)}
													/>
												</Button>
											{:else}
												<Render of={cell.render()} />
											{/if}
										</Table.Head>
									</Subscribe>
								{/each}
							</Table.Row>
						</Subscribe>
					{/each}
				</Table.Header>
				<Table.Body {...$tableBodyAttrs}>
					{#each $pageRows as row (row.id)}
						<Subscribe rowAttrs={row.attrs()} let:rowAttrs>
							<Table.Row {...rowAttrs} data-state={$selectedDataIds[row.id] && 'selected'}>
								{#each row.cells as cell (cell.id)}
									<Subscribe attrs={cell.attrs()} let:attrs>
										<Table.Cell class="[&:has([role=checkbox])]:pl-3" {...attrs}>
											<Render of={cell.render()} />
										</Table.Cell>
									</Subscribe>
								{/each}
							</Table.Row>
						</Subscribe>
					{/each}
				</Table.Body>
			</Table.Root>
		</div>
		{#if showPagination}
			<div class="flex items-center justify-between px-0">
				<div class="text-muted-foreground flex-1 text-sm">
					{$rows.length} row(s)
				</div>
				<div class="flex items-center space-x-6 lg:space-x-8">
					<div class="flex items-center space-x-2">
						<p class="text-sm font-medium">Rows per page</p>
						<Select.Root
							onSelectedChange={(selected) => pageSize.set(Number(selected?.value))}
							selected={{ value: 10, label: '10' }}
						>
							<Select.Trigger class="h-8 w-[70px]">
								<Select.Value placeholder="Select page size" />
							</Select.Trigger>
							<Select.Content>
								<Select.Item value="10">10</Select.Item>
								<Select.Item value="20">20</Select.Item>
								<Select.Item value="30">30</Select.Item>
								<Select.Item value="40">40</Select.Item>
								<Select.Item value="50">50</Select.Item>
								<Select.Item value="100">100</Select.Item>
							</Select.Content>
						</Select.Root>
					</div>
					<div class="flex w-[100px] items-center justify-center text-sm font-medium">
						Page {$pageIndex + 1} of {$pageCount}
					</div>
					<div class="flex items-center space-x-2">
						<Button
							variant="outline"
							class="hidden h-8 w-8 p-0 lg:flex"
							on:click={() => ($pageIndex = 0)}
							disabled={!$hasPreviousPage}
						>
							<span class="sr-only">Go to first page</span>
							<ChevronsLeft size={15} />
						</Button>
						<Button
							variant="outline"
							class="h-8 w-8 p-0"
							on:click={() => ($pageIndex = $pageIndex - 1)}
							disabled={!$hasPreviousPage}
						>
							<span class="sr-only">Go to previous page</span>
							<ChevronLeft size={15} />
						</Button>
						<Button
							variant="outline"
							class="h-8 w-8 p-0"
							disabled={!$hasNextPage}
							on:click={() => ($pageIndex = $pageIndex + 1)}
						>
							<span class="sr-only">Go to next page</span>
							<ChevronRight size={15} />
						</Button>
						<Button
							variant="outline"
							class="hidden h-8 w-8 p-0 lg:flex"
							disabled={!$hasNextPage}
							on:click={() => ($pageIndex = Math.ceil($rows.length / $pageRows.length) - 1)}
						>
							<span class="sr-only">Go to last page</span>
							<ChevronsRight size={15} />
						</Button>
					</div>
				</div>
			</div>
		{/if}
	</div>
</div>

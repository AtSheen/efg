<script lang="ts">
	import * as Table from '$lib/components/ui/table/index.js';

	export let data: Record<string, any>[] = [];
	export let caption: string = 'Data Overview';
	export let excludeColumns: string[] = [];

	$: columns =
		data.length > 0 ? Object.keys(data[0]).filter((key) => !excludeColumns.includes(key)) : [];

	function formatValue(value: any): string {
		if (typeof value === 'number') {
			return value.toString();
		}
		return String(value);
	}
</script>

{#if data.length > 0}
	<Table.Root class="h-fit">
		<Table.Header>
			<Table.Row>
				{#each columns as column}
					<Table.Head>{column}</Table.Head>
				{/each}
			</Table.Row>
		</Table.Header>
		<Table.Body>
			{#each data as row, i (i)}
				<Table.Row>
					{#each columns as column}
						<Table.Cell>{formatValue(row[column])}</Table.Cell>
					{/each}
				</Table.Row>
			{/each}
		</Table.Body>
	</Table.Root>
{/if}

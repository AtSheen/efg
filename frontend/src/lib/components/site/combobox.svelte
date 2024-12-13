<script lang="ts">
	import Check from 'lucide-svelte/icons/check';
	import ChevronsUpDown from 'lucide-svelte/icons/chevrons-up-down';
	import * as Command from '$lib/components/ui/command';
	import * as Popover from '$lib/components/ui/popover';
	import { Button } from '$lib/components/ui/button';
	import { cn } from '$lib/utils.js';
	import { tick } from 'svelte';
	import { Label } from '../ui/label';

	export let data: {
		value: string;
		label: string;
	}[];

	export let placeholder: string = '';

	let open = false;
	export let value = '';

	$: selectedValue = data.find((f) => f.value === value)?.label ?? placeholder;

	// We want to refocus the trigger button when the user selects
	// an item from the list so users can continue navigating the
	// rest of the form with the keyboard.
	function closeAndFocusTrigger(triggerId: string) {
		open = false;
		tick().then(() => {
			document.getElementById(triggerId)?.focus();
		});
	}
</script>

<Popover.Root bind:open let:ids>
	<Popover.Trigger asChild let:builder>
		<div class="flex flex-grow flex-col gap-3">
			<Label><b>{placeholder}:</b></Label>
			<Button
				builders={[builder]}
				variant="outline"
				role="combobox"
				aria-expanded={open}
				class="h-9 w-full justify-between"
			>
				{selectedValue}
				<ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
			</Button>
		</div>
	</Popover.Trigger>

	<Popover.Content class="w-[325px] p-0" sideOffset={5}>
		<Command.Root>
			<Command.Input placeholder="Search VAT (%)..." class="h-9" />
			<Command.Empty>No results found.</Command.Empty>
			<Command.Group>
				{#each data as dataItem (dataItem.value)}
					<Command.Item
						class="h-9"
						value={dataItem.value}
						onSelect={(currentValue) => {
							if (currentValue === value) {
								value = '';
								closeAndFocusTrigger(ids.trigger);
								return;
							}

							value = currentValue;
							closeAndFocusTrigger(ids.trigger);
						}}
					>
						<Check class={cn('mr-2 h-4 w-4', value !== dataItem.value && 'text-transparent')} />
						{dataItem.label}
					</Command.Item>
				{/each}
			</Command.Group>
		</Command.Root>
	</Popover.Content>
</Popover.Root>

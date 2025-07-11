import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { DndContext, closestCorners } from "@dnd-kit/core";
import { useEffect } from "react";
import Column from "./Column";

const fetchLeads = async () => {
  const res = await fetch("/graphql", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: `query { leads { id sender subject score stage } }`,
    }),
  });
  const json = await res.json();
  return json.data.leads;
};

const updateLeadStage = async ({ leadId, newStage }) => {
  const res = await fetch("/graphql", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: `
        mutation UpdateLeadStage($leadId: Int!, $newStage: String!) {
          updateLeadStage(leadId: $leadId, newStage: $newStage) {
            id
            stage
          }
        }
      `,
      variables: { leadId: parseInt(leadId), newStage },
    }),
  });
  const json = await res.json();
  return json.data.updateLeadStage;
};

export default function KanbanBoard() {
  const queryClient = useQueryClient();
  const { data: leads, isLoading } = useQuery({ queryKey: ["leads"], queryFn: fetchLeads });

  const mutation = useMutation({ 
    mutationFn: updateLeadStage, 
    onSuccess: (updatedLead) => {
        queryClient.setQueryData(["leads"], (oldLeads) => {
            return oldLeads.map(lead => lead.id === updatedLead.id ? { ...lead, stage: updatedLead.stage } : lead);
        });
    }
  });

  useEffect(() => {
    const eventSource = new EventSource("/sse/leads");
    eventSource.onmessage = (event) => {
      const newLead = JSON.parse(event.data);
      queryClient.setQueryData(["leads"], (oldLeads) => [...(oldLeads || []), newLead]);
    };
    return () => eventSource.close();
  }, [queryClient]);

  const handleDragEnd = (event) => {
    const { active, over } = event;
    if (over && active.id !== over.id) {
        const leadId = active.id;
        const newStage = over.id;
        const currentLead = leads.find(l => l.id === leadId);

        if (currentLead && currentLead.stage !== newStage) {
            mutation.mutate({ leadId, newStage });
        }
    }
  };

  if (isLoading) return <div>Loading...</div>;

  const stages = ["NEW", "QUALIFIED", "WON"];
  const leadsByStage = stages.reduce((acc, stage) => {
    acc[stage] = (leads || []).filter((lead) => lead.stage === stage);
    return acc;
  }, {});

  return (
    <DndContext collisionDetection={closestCorners} onDragEnd={handleDragEnd}>
      <div className="grid grid-cols-3 gap-4 p-4">
        {stages.map((stage) => (
          <Column key={stage} title={stage} cards={leadsByStage[stage]} />
        ))}
      </div>
    </DndContext>
  );
}
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import KanbanBoard from "./src/components/KanBanBoard";

const queryClient = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <KanbanBoard />
    </QueryClientProvider>
  );
}
import { useState, useEffect } from "react"; // Añadimos hooks
import DashboardHeader from "@/components/dashboard/DashboardHeader";
import MetricsGrid from "@/components/dashboard/MetricsGrid";
import PriceChart from "@/components/dashboard/PriceChart";
import NewsSidebar from "@/components/dashboard/NewsSidebar";

const Index = () => {
  // 1. Creamos un estado para los datos
  const [data, setData] = useState<any>(null);

  // 2. Función para cargar el JSON dinámicamente
  useEffect(() => {
    const loadData = () => {
      // El ?t= evita que el navegador use una versión vieja (caché)
      fetch("/data.json?t=" + new Date().getTime())
        .then((res) => res.json())
        .then((json) => setData(json))
        .catch((err) => console.error("Error cargando datos:", err));
    };

    loadData(); // Carga inicial
    const interval = setInterval(loadData, 30000); // Recarga cada 30 segundos solo
    return () => clearInterval(interval);
  }, []);

  // 3. Si aún no hay datos, mostramos un aviso
  if (!data) {
    return <div className="flex h-screen items-center justify-center">Cargando datos de la terminal...</div>;
  }

  // 4. Desestructuramos los datos que han llegado del fetch
  const { ticker, metricas_fundamentales, grafico, noticias } = data;
  
  const firstPrice = grafico.precios[0];
  const lastPrice = grafico.precios[grafico.precios.length - 1];
  const priceChange = ((lastPrice - firstPrice) / firstPrice) * 100;
  const recommendation = metricas_fundamentales["Recomendación Analistas"] || "Hold";

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader 
        ticker={ticker} 
        recommendation={recommendation}
        priceChange={priceChange}
      />
      
      <main className="p-6 space-y-6">
        <section>
          <MetricsGrid metrics={metricas_fundamentales} />
        </section>
        
        <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <PriceChart 
              fechas={grafico.fechas} 
              precios={grafico.precios} 
            />
          </div>
          
          <div className="lg:col-span-1">
            <NewsSidebar noticias={noticias} />
          </div>
        </section>
      </main>
    </div>
  );
};

export default Index;
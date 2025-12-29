import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, BarChart3, DollarSign, Activity } from "lucide-react";

interface MetricsGridProps {
  metrics: Record<string, string | number>;
}

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  "Recomendación Analistas": TrendingUp,
  "default": BarChart3,
};

const MetricsGrid = ({ metrics }: MetricsGridProps) => {
  const entries = Object.entries(metrics);
  
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {entries.map(([key, value]) => {
        const Icon = iconMap[key] || iconMap["default"];
        const isRecommendation = key === "Recomendación Analistas";
        const isBuy = typeof value === "string" && value.toLowerCase() === "buy";
        
        return (
          <Card 
            key={key} 
            className="bg-card/80 border-border/50 backdrop-blur-sm hover:border-primary/30 transition-colors card-glow"
          >
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {key}
              </CardTitle>
              <Icon className={`h-4 w-4 ${isRecommendation && isBuy ? "text-primary" : "text-muted-foreground"}`} />
            </CardHeader>
            <CardContent>
              <div className={`text-2xl font-bold font-mono ${
                isRecommendation 
                  ? isBuy 
                    ? "text-primary" 
                    : "text-destructive"
                  : "text-foreground"
              }`}>
                {value}
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
};

export default MetricsGrid;
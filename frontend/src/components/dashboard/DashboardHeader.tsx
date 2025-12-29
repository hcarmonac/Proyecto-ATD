import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown } from "lucide-react";

interface DashboardHeaderProps {
  ticker: string;
  recommendation: string;
  priceChange: number;
}

const DashboardHeader = ({ ticker, recommendation, priceChange }: DashboardHeaderProps) => {
  const isPositive = priceChange >= 0;
  
  return (
    <header className="flex items-center justify-between border-b border-border bg-card/50 backdrop-blur-sm px-6 py-4">
      <div className="flex items-center gap-4">
        <h1 className="text-4xl font-bold font-mono tracking-tight">
          <span className={isPositive ? "text-primary glow-green" : "text-destructive glow-red"}>
            {ticker}
          </span>
        </h1>
        <div className="flex items-center gap-2">
          {isPositive ? (
            <TrendingUp className="h-5 w-5 text-primary" />
          ) : (
            <TrendingDown className="h-5 w-5 text-destructive" />
          )}
          <span className={`font-mono text-sm ${isPositive ? "text-primary" : "text-destructive"}`}>
            {isPositive ? "+" : ""}{priceChange.toFixed(2)}%
          </span>
        </div>
      </div>
      
      <Badge 
        variant="outline" 
        className={`
          px-3 py-1 text-sm font-medium border-2
          ${recommendation.toLowerCase() === 'buy' 
            ? 'border-primary text-primary bg-primary/10' 
            : recommendation.toLowerCase() === 'sell'
            ? 'border-destructive text-destructive bg-destructive/10'
            : 'border-warning text-warning bg-warning/10'
          }
        `}
      >
        {recommendation}
      </Badge>
    </header>
  );
};

export default DashboardHeader;
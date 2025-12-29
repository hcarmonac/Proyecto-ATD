import { useMemo } from "react";
import { format, parseISO } from "date-fns";
import { es } from "date-fns/locale";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  AreaChart,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface PriceChartProps {
  fechas: string[];
  precios: number[];
}

const PriceChart = ({ fechas, precios }: PriceChartProps) => {
  const data = useMemo(() => {
    return fechas.map((fecha, index) => ({
      date: fecha,
      price: precios[index],
      formattedDate: format(parseISO(fecha), "dd MMM yyyy", { locale: es }),
    }));
  }, [fechas, precios]);

  const isPositiveTrend = precios[precios.length - 1] > precios[0];
  const chartColor = isPositiveTrend 
    ? "hsl(142, 76%, 45%)" 
    : "hsl(0, 72%, 51%)";
  
  const minPrice = Math.min(...precios);
  const maxPrice = Math.max(...precios);
  const priceRange = maxPrice - minPrice;
  const yAxisMin = Math.floor(minPrice - priceRange * 0.05);
  const yAxisMax = Math.ceil(maxPrice + priceRange * 0.05);

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-card border border-border rounded-lg p-3 shadow-lg backdrop-blur-sm">
          <p className="text-muted-foreground text-xs mb-1">
            {payload[0]?.payload?.formattedDate}
          </p>
          <p className={`font-mono font-bold text-lg ${isPositiveTrend ? "text-primary" : "text-destructive"}`}>
            ${payload[0]?.value?.toFixed(2)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <Card className="bg-card/80 border-border/50 backdrop-blur-sm card-glow h-full">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-medium text-foreground flex items-center gap-2">
          Evolución del Precio
          <span className={`text-sm font-mono ${isPositiveTrend ? "text-primary" : "text-destructive"}`}>
            ${precios[0]?.toFixed(2)} → ${precios[precios.length - 1]?.toFixed(2)}
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent className="h-[400px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={chartColor} stopOpacity={0.3} />
                <stop offset="95%" stopColor={chartColor} stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid 
              strokeDasharray="3 3" 
              stroke="hsl(220, 20%, 20%)" 
              vertical={false}
            />
            <XAxis
              dataKey="formattedDate"
              stroke="hsl(215, 20%, 65%)"
              fontSize={11}
              tickLine={false}
              axisLine={false}
              tick={{ fill: "hsl(215, 20%, 65%)" }}
              interval={Math.floor(data.length / 6)}
            />
            <YAxis
              domain={[yAxisMin, yAxisMax]}
              stroke="hsl(215, 20%, 65%)"
              fontSize={11}
              tickLine={false}
              axisLine={false}
              tick={{ fill: "hsl(215, 20%, 65%)" }}
              tickFormatter={(value) => `$${value}`}
              width={60}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey="price"
              stroke={chartColor}
              strokeWidth={2}
              fill="url(#colorPrice)"
              dot={false}
              activeDot={{
                r: 6,
                fill: chartColor,
                stroke: "hsl(220, 25%, 10%)",
                strokeWidth: 2,
              }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};

export default PriceChart;
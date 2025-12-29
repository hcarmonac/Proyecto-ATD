import { format, parseISO } from "date-fns";
import { es } from "date-fns/locale";
import { ExternalLink, Newspaper } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";

interface NewsItem {
  fecha: string;
  titulo: string;
  enlace: string;
}

interface NewsSidebarProps {
  noticias: NewsItem[];
}

const NewsSidebar = ({ noticias }: NewsSidebarProps) => {
  return (
    <Card className="bg-card/80 border-border/50 backdrop-blur-sm card-glow h-full flex flex-col">
      <CardHeader className="pb-3 flex-shrink-0">
        <CardTitle className="text-lg font-medium text-foreground flex items-center gap-2">
          <Newspaper className="h-5 w-5 text-primary" />
          Últimas Noticias
          <span className="text-xs text-muted-foreground font-normal ml-auto">
            {noticias.length} artículos
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 overflow-hidden p-0">
        <ScrollArea className="h-[500px] px-6">
          <div className="space-y-1 pb-4">
            {noticias.map((noticia, index) => (
              <div key={index}>
                <a
                  href={noticia.enlace}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group block py-3 hover:bg-secondary/30 rounded-lg px-2 -mx-2 transition-colors"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-muted-foreground mb-1 font-mono">
                        {format(parseISO(noticia.fecha), "dd MMM yyyy", { locale: es })}
                      </p>
                      <h3 className="text-sm text-foreground group-hover:text-primary transition-colors line-clamp-2 leading-relaxed">
                        {noticia.titulo}
                      </h3>
                    </div>
                    <ExternalLink className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors flex-shrink-0 mt-1" />
                  </div>
                </a>
                {index < noticias.length - 1 && (
                  <Separator className="bg-border/50" />
                )}
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};

export default NewsSidebar;
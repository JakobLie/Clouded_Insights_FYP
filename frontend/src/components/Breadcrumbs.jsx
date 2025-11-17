"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

/**
 * Configure explicit breadcrumb trails for known routes.
 * Each item: { label: string, href?: string }
 * If href is omitted, it will render as the current/last crumb (non-clickable).
 */
const ROUTE_BREADCRUMBS = {
  "/profit": [{ label: "Profit" }],
  "/cost": [{ label: "Cost" }],
  "/cost/drill-down": [
    { label: "Cost", href: "/cost" },
    { label: "Drill-Down" },
  ],
  "/sales": [{ label: "Sales" }],
  "/sales/drill-down": [
    { label: "Sales", href: "/sales" },
    { label: "Drill-Down" },
  ],
  "/notifications": [{ label: "Notifications" }],
  "/setup": [{ label: "Setup" }],
};

/**
 * Optional: pretty label for a URL segment when auto-generating.
 * e.g. "drill-down" -> "Drill-Down"
 */
const LABEL_OVERRIDES = {
  "drill-down": "Drill-Down",
};

function autoBuildFromPath(pathname) {
  // Split and clean segments
  const segments = pathname
    .split("/")
    .filter(Boolean); // remove empty strings

  // Build incremental hrefs for each segment (for linking parents)
  const crumbs = segments.map((seg, idx) => {
    const href = "/" + segments.slice(0, idx + 1).join("/");
    const raw = seg.replace(/-/g, " ");
    const label =
      LABEL_OVERRIDES[seg] ||
      raw
        .split(" ")
        .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
        .join(" ");

    return { label, href };
  });

  // Make last crumb non-clickable
  if (crumbs.length) delete crumbs[crumbs.length - 1].href;
  return crumbs;
}

export default function Breadcrumbs({
  items,                // optional: override crumbs entirely [{label, href}]
  showHome = false,     // set true to prefix a Home crumb
  homeLabel = "Home",
  homeHref = "/",
  separator = "›",      // visual separator
  className = "",
}) {
  const pathname = usePathname() || "/";

  // Use explicit config first, else auto-generate
  const fromConfig = ROUTE_BREADCRUMBS[pathname];
  let crumbs = items || fromConfig || autoBuildFromPath(pathname);

  // Optionally add a home crumb at the start
  if (showHome) {
    crumbs = [{ label: homeLabel, href: homeHref }, ...crumbs];
  }

  return (
    <nav aria-label="Breadcrumb" className={`text-sm ${className}`}>
      <ol className="flex flex-wrap items-center gap-2 text-muted-foreground">
        {crumbs.map((c, i) => {
          const isLast = i === crumbs.length - 1;
          return (
            <li key={i} className="flex items-center gap-2">
              {c.href && !isLast ? (
                <Link
                  href={c.href}
                  className="text-3xl text-blue-600 hover:underline"
                >
                  {c.label}
                </Link>
              ) : (
                <span className={isLast ? "text-3xl text-foreground font-medium text-gray-400" : ""}>
                  {c.label}
                </span>
              )}
              {!isLast && <span className="opacity-60 text-3xl">{separator}</span>}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

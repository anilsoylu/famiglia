// app/paywall.tsx (excerpt)
import { useEffect, useState } from "react";
import { Pressable, Text, View } from "react-native";
import { router, useLocalSearchParams } from "expo-router";
import Purchases from "react-native-purchases";
import { posthog } from "@/lib/analytics";

export default function Paywall() {
  const { source } = useLocalSearchParams<{ source: string }>();
  const [seconds, setSeconds] = useState(600); // "offer ends in 10:00", restarts on every open
  const [plan, setPlan] = useState<"yearly" | "monthly">("yearly");
  const [trialReminder, setTrialReminder] = useState(false); // off by default

  useEffect(() => {
    posthog.capture("paywall_view", { source }); // was "paywall_viewed" before 2.5.0
    const t = setInterval(() => setSeconds((s) => Math.max(0, s - 1)), 1000);
    return () => clearInterval(t);
  }, []);

  const buy = async () => {
    posthog.capture("purchase_started", { source, product: plan === "yearly" ? "stepwise_yearly_3999" : "stepwise_monthly_499" });
    const pkg = plan === "yearly" ? offerings.current.annual : offerings.current.monthly;
    await Purchases.purchasePackage(pkg);
    router.replace("/home");
  };

  return (
    <View style={styles.container}>
      {/* close: 14px, gray-on-gray, top-left, appears after 3 seconds */}
      <Pressable onPress={() => router.replace("/home")} style={styles.close} hitSlop={2}>
        <Text style={{ fontSize: 14, color: "#C9CCD1" }}>×</Text>
      </Pressable>

      <Text style={styles.headline}>Unlock Stepwise Plus</Text>
      <Text style={styles.timer}>Special offer ends in {formatMMSS(seconds)}</Text>

      <PlanCard selected={plan === "yearly"} onPress={() => setPlan("yearly")}
        title="Yearly" subtitle="7 days free" badge="BEST VALUE" />
      <PlanCard selected={plan === "monthly"} onPress={() => setPlan("monthly")}
        title="Monthly" subtitle="$4.99 / month" />

      <ToggleRow label="Remind me before my trial ends" value={trialReminder} onChange={setTrialReminder} />

      <Pressable onPress={buy} style={styles.cta}>
        <Text style={styles.ctaText}>{plan === "yearly" ? "Start free trial" : "Continue"}</Text>
      </Pressable>
      {/* no price/charge-date line under the button */}

      <FooterLinks items={["Restore", "Terms", "Privacy"]} />
    </View>
  );
}

import os
import re

def parseTierFiles(sourcesDir, skillsData):
    # Parse tier_1.md to tier_6.md
    for tierNum in range(1, 7):
        filePath = os.path.join(sourcesDir, f"tier_{tierNum}.md")
        if not os.path.exists(filePath):
            continue
        
        content = open(filePath, "r").read()
        # Split by skills (## Skill:)
        skillBlocks = content.split("## Skill: ")
        for block in skillBlocks[1:]:
            lines = block.split("\n")
            skillId = lines[0].strip().replace("`", "")
            
            if skillId not in skillsData:
                skillsData[skillId] = {
                    "id": skillId,
                    "tier": f"{tierNum}★",
                    "evidenceRows": [],
                    "benchmarks": [],
                    "reviews": [],
                    "papers": [],
                    "blogs": [],
                    "videos": [],
                    "verifications": []
                }
            
            # Extract basic properties
            for line in lines[1:]:
                if line.startswith("- **Name:**"):
                    skillsData[skillId]["name"] = line.split("- **Name:**")[1].strip()
                elif line.startswith("- **Contributor:**"):
                    skillsData[skillId]["contributor"] = line.split("- **Contributor:**")[1].strip().replace("`", "")
                elif line.startswith("- **Primary GitHub Repository:**"):
                    skillsData[skillId]["primaryRepo"] = line.split("- **Primary GitHub Repository:**")[1].strip()

            # Extract raw evidence rows (#### E1: ...)
            evSplit = block.split("#### E")
            for evBlock in evSplit[1:]:
                evLines = evBlock.split("\n")
                evHeader = evLines[0].strip()
                evContent = []
                for evLine in evLines[1:]:
                    if evLine.strip() == "---" or evLine.startswith("## Skill:"):
                        break
                    evContent.append(evLine)
                skillsData[skillId]["evidenceRows"].append({
                    "header": f"E{evHeader}",
                    "content": "\n".join(evContent).strip()
                })

def parseCollectorFiles(collectorsDir, skillsData):
    # Parse benchmark results
    benchPath = os.path.join(collectorsDir, "technical", "benchmark_results.md")
    if os.path.exists(benchPath):
        content = open(benchPath, "r").read()
        blocks = content.split("### ")
        for block in blocks[1:]:
            lines = block.split("\n")
            title = lines[0].strip().replace("`", "")
            # Find matching skillId
            for skillId in skillsData.keys():
                if skillId in title or title in skillId:
                    skillsData[skillId]["benchmarks"].append(block)

    # Parse reviews & audits
    reviewPath = os.path.join(collectorsDir, "technical", "peer_reviews_audits.md")
    if os.path.exists(reviewPath):
        content = open(reviewPath, "r").read()
        blocks = content.split("## ")
        for block in blocks[1:]:
            lines = block.split("\n")
            title = lines[0].strip().replace("`", "")
            for skillId in skillsData.keys():
                if skillId in title or title in skillId:
                    skillsData[skillId]["reviews"].append(block)

    # Parse academic papers
    academicPath = os.path.join(collectorsDir, "technical", "academic_papers.md")
    if os.path.exists(academicPath):
        content = open(academicPath, "r").read()
        blocks = content.split("### ")
        for block in blocks[1:]:
            lines = block.split("\n")
            title = lines[0].strip().replace("`", "")
            for skillId in skillsData.keys():
                if skillId in title or title in skillId:
                    skillsData[skillId]["papers"].append(block)

    # Parse blogs and newsletters
    blogPath = os.path.join(collectorsDir, "social", "blogs_newsletters.md")
    if os.path.exists(blogPath):
        content = open(blogPath, "r").read()
        blocks = content.split("### ")
        for block in blocks[1:]:
            lines = block.split("\n")
            title = lines[0].strip().replace("`", "")
            for skillId in skillsData.keys():
                if skillId in title or title in skillId:
                    skillsData[skillId]["blogs"].append(block)

    # Parse YouTube showcases
    youtubePath = os.path.join(collectorsDir, "social", "youtube_showcases.md")
    if os.path.exists(youtubePath):
        content = open(youtubePath, "r").read()
        blocks = content.split("## ")
        for block in blocks[1:]:
            lines = block.split("\n")
            title = lines[0].strip()
            # Match contributor/handler name
            for skillId in skillsData.keys():
                contributor = skillsData[skillId]["contributor"]
                if contributor in title:
                    skillsData[skillId]["videos"].append(block)

    # Parse verifications
    verifPath = os.path.join(collectorsDir, "verification", "verification_report.md")
    if os.path.exists(verifPath):
        content = open(verifPath, "r").read()
        # Find lines in table matching skill
        for skillId in skillsData.keys():
            matches = []
            for line in content.split("\n"):
                if skillId in line:
                    matches.append(line)
            if matches:
                skillsData[skillId]["verifications"].extend(matches)

def writeUnifiedLake(outputPath, skillsData):
    out = open(outputPath, "w")
    out.write("# Gaia Trust Methodology: Unified Evidence Data Lake\n\n")
    out.write("This unified data lake compiles all evidence dumps (Tiers 1★ to 6★) and specialized collector findings into a single source of truth indexed by skill ID.\n\n")
    
    out.write("## Table of Contents\n\n")
    # Sort skills by tier (descending) then by ID
    def getTierWeight(tierStr):
        return int(tierStr.replace("★", ""))
    
    sortedSkills = sorted(skillsData.values(), key=lambda x: (-getTierWeight(x["tier"]), x["id"]))
    
    for s in sortedSkills:
        out.write(f"- [{s['id']} (Tier {s['tier']})](#skill-{s['id'].replace('/', '').replace('.', '')})\n")
    out.write("\n---\n\n")
    
    for s in sortedSkills:
        cleanAnchor = s['id'].replace('/', '').replace('.', '')
        out.write(f"## Skill: <a name=\"skill-{cleanAnchor}\"></a>`{s['id']}`\n\n")
        out.write(f"- **Name:** {s.get('name', 'N/A')}\n")
        out.write(f"- **Contributor:** `{s.get('contributor', 'N/A')}`\n")
        out.write(f"- **Tier:** {s['tier']}\n")
        if "primaryRepo" in s:
            out.write(f"- **Primary Repository:** {s['primaryRepo']}\n")
        out.write("\n")
        
        # 1. Base Evidence Rows
        out.write("### Base Evidence Rows\n\n")
        if s["evidenceRows"]:
            for ev in s["evidenceRows"]:
                out.write(f"#### {ev['header']}\n{ev['content']}\n\n")
        else:
            out.write("*No base evidence rows.*\n\n")
            
        # 2. Benchmarks
        if s["benchmarks"]:
            out.write("### Benchmark Evaluations\n\n")
            for b in s["benchmarks"]:
                # Strip heading
                lines = b.split("\n")
                out.write("\n".join(lines[1:]).strip() + "\n\n")
                
        # 3. Peer Reviews & Audits
        if s["reviews"]:
            out.write("### Peer Reviews & Audits\n\n")
            for r in s["reviews"]:
                lines = r.split("\n")
                out.write("\n".join(lines[1:]).strip() + "\n\n")
                
        # 4. Academic Papers
        if s["papers"]:
            out.write("### Academic Papers & Preprints\n\n")
            for p in s["papers"]:
                lines = p.split("\n")
                out.write("\n".join(lines[1:]).strip() + "\n\n")
                
        # 5. Blogs & Newsletters
        if s["blogs"]:
            out.write("### Blog & Newsletter Signals\n\n")
            for bl in s["blogs"]:
                lines = bl.split("\n")
                out.write("\n".join(lines[1:]).strip() + "\n\n")
                
        # 6. YouTube Showcases
        if s["videos"]:
            out.write("### YouTube Showcase Videos\n\n")
            for v in s["videos"]:
                lines = v.split("\n")
                out.write("\n".join(lines[1:]).strip() + "\n\n")

        # 7. Verification Status
        if s["verifications"]:
            out.write("### Verification Audits\n\n")
            out.write("| Skill ID / Contributor | Evidence Source / URL | Status | Category / Finding |\n")
            out.write("| :--- | :--- | :--- | :--- |\n")
            for ver in s["verifications"]:
                out.write(ver + "\n")
            out.write("\n")
            
        out.write("---\n\n")
        
    out.close()

def main():
    sourcesDir = "founder/sources"
    collectorsDir = "founder/sources/collectors"
    lakeDir = "founder/sources/data_lake"
    
    os.makedirs(lakeDir, exist_ok=True)
    
    skillsData = {}
    print("Parsing tier dumps...")
    parseTierFiles(sourcesDir, skillsData)
    print("Parsing collector files...")
    parseCollectorFiles(collectorsDir, skillsData)
    
    outputPath = os.path.join(lakeDir, "unified_evidence_lake.md")
    print(f"Writing unified data lake to {outputPath}...")
    writeUnifiedLake(outputPath, skillsData)
    print("Data lake compilation complete.")

if __name__ == "__main__":
    main()

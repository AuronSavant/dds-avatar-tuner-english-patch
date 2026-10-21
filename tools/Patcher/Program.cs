// Patches the game's Assembly-CSharp.dll so it calls into DDSA_EN.dll (the English patch hooks).
//   Patcher publicize <orig Assembly-CSharp.dll> <out.dll>
//   Patcher patch     <orig Assembly-CSharp.dll> <DDSA_EN.dll> <out.dll>
using System;
using System.IO;
using System.Linq;
using Mono.Cecil;
using Mono.Cecil.Cil;

static class Program
{
    static int Main(string[] args)
    {
        try
        {
            if (args.Length == 3 && args[0] == "publicize")
            {
                var asm = Load(args[1]);
                Publicize(asm.MainModule);
                asm.Write(args[2]);
            }
            else if (args.Length == 4 && args[0] == "patch")
            {
                var asm = Load(args[1]);
                var hooks = AssemblyDefinition.ReadAssembly(args[2]);
                Publicize(asm.MainModule);
                Patch(asm.MainModule, hooks.MainModule);
                asm.Write(args[3]);
            }
            else
            {
                Console.Error.WriteLine("usage: Patcher publicize <in> <out> | patch <in> <hooks> <out>");
                return 2;
            }
            Console.WriteLine("ok");
            return 0;
        }
        catch (Exception e)
        {
            Console.Error.WriteLine(e);
            return 1;
        }
    }

    static AssemblyDefinition Load(string path)
    {
        var resolver = new DefaultAssemblyResolver();
        resolver.AddSearchDirectory(Path.GetDirectoryName(Path.GetFullPath(path)));
        // read fully into memory so the output may overwrite the input path
        var ms = new MemoryStream(File.ReadAllBytes(path));
        return AssemblyDefinition.ReadAssembly(ms, new ReaderParameters { AssemblyResolver = resolver });
    }

    static TypeDefinition Type(ModuleDefinition m, string fullName)
    {
        var t = m.GetType(fullName);
        if (t == null) throw new Exception("type not found: " + fullName);
        return t;
    }

    static MethodDefinition Method(TypeDefinition t, string name, int paramCount)
    {
        var md = t.Methods.SingleOrDefault(x => x.Name == name && x.Parameters.Count == paramCount);
        if (md == null) throw new Exception("method not found: " + t.FullName + "::" + name);
        return md;
    }

    static void Publicize(ModuleDefinition m)
    {
        var gc = Type(m, "GameCanvas");
        Method(gc, "_eventNewLine", 1).IsPublic = true;
        gc.Fields.Single(f => f.Name == "data_object").IsPublic = true;
        var loc = Type(m, "Steezy.Localize.Localization");
        loc.Fields.Single(f => f.Name == "mDictionary").IsPublic = true;
    }

    static MethodReference Hook(ModuleDefinition m, ModuleDefinition hooks, string name)
    {
        var t = hooks.GetType("DDSA_EN.Hooks");
        return m.ImportReference(t.Methods.Single(x => x.Name == name));
    }

    static void Patch(ModuleDefinition m, ModuleDefinition hooks)
    {
        var gc = Type(m, "GameCanvas");

        // GetResource(string filename, bool nondirect): prologue
        //   sbyte[] o = Hooks.GetResource(filename); if (o != null) return o;
        {
            var md = Method(gc, "GetResource", 2);
            var il = md.Body.GetILProcessor();
            var first = md.Body.Instructions[0];
            var tmp = new VariableDefinition(md.ReturnType);
            md.Body.Variables.Add(tmp);
            il.InsertBefore(first, il.Create(OpCodes.Ldarg_1));
            il.InsertBefore(first, il.Create(OpCodes.Call, Hook(m, hooks, "GetResource")));
            il.InsertBefore(first, il.Create(OpCodes.Stloc, tmp));
            il.InsertBefore(first, il.Create(OpCodes.Ldloc, tmp));
            il.InsertBefore(first, il.Create(OpCodes.Brfalse, first));
            il.InsertBefore(first, il.Create(OpCodes.Ldloc, tmp));
            il.InsertBefore(first, il.Create(OpCodes.Ret));
        }

        // _printEventString(work, mode, str) => Hooks.PrintEventString(this, work, mode, str)
        ReplaceBody(Method(gc, "_printEventString", 3), Hook(m, hooks, "PrintEventString"), true);
        // MakeStringTableBR(text, font, width) => Hooks.MakeStringTableBR(text, font, width)
        ReplaceBody(Method(gc, "MakeStringTableBR", 3), Hook(m, hooks, "MakeStringTableBR"), false);

        // Localization.LoadCSV(): call Hooks.AfterLoadCSV() before every return
        BeforeReturns(Method(Type(m, "Steezy.Localize.Localization"), "LoadCSV", 0), Hook(m, hooks, "AfterLoadCSV"));
        // TitleDataModel.GetTitleData(): return Hooks.FixTitle(result)
        BeforeReturns(Method(Type(m, "TitleDataModel"), "GetTitleData", 0), Hook(m, hooks, "FixTitle"));
        // HowToPlayDataModel.GetHowToPlayImages(): return Hooks.FixHowToPlay(result)
        BeforeReturns(Method(Type(m, "HowToPlayDataModel"), "GetHowToPlayImages", 0), Hook(m, hooks, "FixHowToPlay"));
    }

    static void ReplaceBody(MethodDefinition md, MethodReference target, bool passThis)
    {
        var body = md.Body;
        body.Instructions.Clear();
        body.ExceptionHandlers.Clear();
        body.Variables.Clear();
        var il = body.GetILProcessor();
        if (passThis) il.Append(il.Create(OpCodes.Ldarg_0));
        for (int i = 0; i < md.Parameters.Count; i++)
            il.Append(il.Create(OpCodes.Ldarg, md.Parameters[i]));
        il.Append(il.Create(OpCodes.Call, target));
        il.Append(il.Create(OpCodes.Ret));
    }

    static void BeforeReturns(MethodDefinition md, MethodReference call)
    {
        var il = md.Body.GetILProcessor();
        foreach (var ret in md.Body.Instructions.Where(x => x.OpCode == OpCodes.Ret).ToList())
        {
            // insert the call at the ret's position so branches targeting the ret still run it
            var c = il.Create(OpCodes.Call, call);
            il.InsertBefore(ret, c);
            foreach (var ins in md.Body.Instructions)
            {
                if (ins.Operand == ret && ins != c) ins.Operand = c;
                if (ins.Operand is Instruction[] targets)
                    for (int i = 0; i < targets.Length; i++) if (targets[i] == ret) targets[i] = c;
            }
            foreach (var h in md.Body.ExceptionHandlers)
            {
                if (h.HandlerEnd == ret) h.HandlerEnd = c;
                if (h.TryEnd == ret) h.TryEnd = c;
            }
        }
    }
}

using System.Collections.Generic;
using UnityEngine;
using FullSerializer;

public class UnityObjectConverterExample : MonoBehaviour
{
    public string           SerialisedCustomClass = "";
    public List<Object>     UnityObjectReferences = new List<Object>();
    public CustomClass      CustomClassInstance = new CustomClass();

    private fsSerializer    mSerialiser = null;

    // -------------------------------------------------------------------------------

    void Start()
    {
        mSerialiser = new fsSerializer();
        mSerialiser.AddConverter(new UnityObjectConverter());
        mSerialiser.Context.Set(UnityObjectReferences);
    }

    // -------------------------------------------------------------------------------

   public void Save()
    {
        // We want to fill in a fresh list of references so clear the existing one
        // in case it contains any stale/unused references
        UnityObjectReferences.Clear();

        // Serialise our CustomClass and save it to a string
        fsData data;
        mSerialiser.TrySerialize(typeof(CustomClass), CustomClassInstance, out data).AssertSuccessWithoutWarnings();
        SerialisedCustomClass = fsJsonPrinter.CompressedJson(data);
    }

    // -------------------------------------------------------------------------------

    public void Load()
    {
        // Load our custom CustomClass from its serialised string form, or create a new instance
        if (SerialisedCustomClass != "")
        {
            fsData parsedData = fsJsonParser.Parse(SerialisedCustomClass);
            object deserializedData = null;
            mSerialiser.TryDeserialize(parsedData, typeof(CustomClass), ref deserializedData).AssertSuccessWithoutWarnings();
            CustomClassInstance = (CustomClass)deserializedData;
        }
        else
        {
            CustomClassInstance = new CustomClass();
        }
    }
}
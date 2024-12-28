CREATE TABLE AUG_GovernmentPersonalData (
    ﻿MkID INT,
    LastName NVARCHAR(MAX),
    FirstName NVARCHAR(MAX),
    FullName NVARCHAR(MAX),
    BirthDate NVARCHAR(MAX),
    YearDate FLOAT,
    BirthDateHeb NVARCHAR(MAX),
    DeathDate NVARCHAR(MAX),
    DeathDateHeb NVARCHAR(MAX),
    YearDeathDate FLOAT,
    ImmigrationDate NVARCHAR(MAX),
    BirthCountry NVARCHAR(MAX),
    CityName NVARCHAR(MAX),
    FamilyStatus NVARCHAR(MAX),
    ChildrenNumber FLOAT,
    imgPath NVARCHAR(MAX),
    FK_MKStatus INT,
    FirstLetter NVARCHAR(MAX),
    LU_Gender INT
);

CREATE TABLE AUG_PersonIdToMkId (
    PersonID INT,
    MkID INT
);

CREATE TABLE KNS_Agenda (
    AgendaID INT,
    Number FLOAT,
    ClassificationID FLOAT,
    ClassificationDesc NVARCHAR(MAX),
    LeadingAgendaID FLOAT,
    KnessetNum INT,
    Name NVARCHAR(MAX),
    SubTypeID INT,
    SubTypeDesc NVARCHAR(MAX),
    StatusID INT,
    InitiatorPersonID FLOAT,
    GovRecommendationID FLOAT,
    GovRecommendationDesc FLOAT,
    PresidentDecisionDate NVARCHAR(MAX),
    PostopenmentReasonID FLOAT,
    PostopenmentReasonDesc NVARCHAR(MAX),
    CommitteeID FLOAT,
    RecommendCommitteeID FLOAT,
    MinisterPersonID FLOAT,
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_Bill (
    BillID INT,
    KnessetNum INT,
    Name NVARCHAR(MAX),
    SubTypeID INT,
    SubTypeDesc NVARCHAR(MAX),
    PrivateNumber FLOAT,
    CommitteeID FLOAT,
    StatusID INT,
    Number FLOAT,
    PostponementReasonID FLOAT,
    PostponementReasonDesc NVARCHAR(MAX),
    PublicationDate NVARCHAR(MAX),
    MagazineNumber FLOAT,
    PageNumber FLOAT,
    IsContinuationBill FLOAT,
    SummaryLaw NVARCHAR(MAX),
    PublicationSeriesID FLOAT,
    PublicationSeriesDesc NVARCHAR(MAX),
    PublicationSeriesFirstCall NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_BillHistoryInitiator (
    BillHistoryInitiatorID INT,
    BillID INT,
    PersonID INT,
    IsInitiator INT,
    StartDate NVARCHAR(MAX),
    EndDate NVARCHAR(MAX),
    ReasonID FLOAT,
    ReasonDesc NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_BillInitiator (
    BillInitiatorID INT,
    BillID INT,
    PersonID INT,
    IsInitiator FLOAT,
    Ordinal INT,
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_BillName (
    BillNameID INT,
    BillID INT,
    Name NVARCHAR(MAX),
    NameHistoryTypeID INT,
    NameHistoryTypeDesc NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_BillSplit (
    BillSplitID INT,
    MainBillID INT,
    SplitBillID INT,
    Name NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_BillUnion (
    BillUnionID INT,
    MainBillID INT,
    UnionBillID INT,
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_CmtSessionItem (
    CmtSessionItemID INT,
    ItemID INT,
    CommitteeSessionID INT,
    Ordinal FLOAT,
    StatusID FLOAT,
    Name NVARCHAR(MAX),
    ItemTypeID INT,
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_CmtSiteCode (
    CmtSiteCode INT,
    KnsID INT,
    SiteId INT
);

CREATE TABLE KNS_Committee (
    CommitteeID INT,
    Name NVARCHAR(MAX),
    CategoryID FLOAT,
    CategoryDesc NVARCHAR(MAX),
    KnessetNum INT,
    CommitteeTypeID INT,
    CommitteeTypeDesc NVARCHAR(MAX),
    Email NVARCHAR(MAX),
    StartDate NVARCHAR(MAX),
    FinishDate NVARCHAR(MAX),
    AdditionalTypeID FLOAT,
    AdditionalTypeDesc NVARCHAR(MAX),
    ParentCommitteeID FLOAT,
    CommitteeParentName NVARCHAR(MAX),
    IsCurrent INT,
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_CommitteeSession (
    CommitteeSessionID INT,
    Number FLOAT,
    KnessetNum INT,
    TypeID INT,
    TypeDesc NVARCHAR(MAX),
    CommitteeID INT,
    StatusID INT,
    StatusDesc NVARCHAR(MAX),
    Location NVARCHAR(MAX),
    SessionUrl NVARCHAR(MAX),
    BroadcastUrl NVARCHAR(MAX),
    StartDate NVARCHAR(MAX),
    FinishDate NVARCHAR(MAX),
    Note NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_DocumentAgenda (
    DocumentAgendaID INT,
    AgendaID INT,
    GroupTypeID INT,
    GroupTypeDesc NVARCHAR(MAX),
    ApplicationID INT,
    ApplicationDesc NVARCHAR(MAX),
    FilePath NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_DocumentBill (
    DocumentBillID INT,
    BillID INT,
    GroupTypeID INT,
    GroupTypeDesc NVARCHAR(MAX),
    ApplicationID INT,
    ApplicationDesc NVARCHAR(MAX),
    FilePath NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_DocumentCommitteeSession (
    DocumentCommitteeSessionID INT,
    CommitteeSessionID INT,
    GroupTypeID INT,
    GroupTypeDesc NVARCHAR(MAX),
    ApplicationID INT,
    ApplicationDesc NVARCHAR(MAX),
    FilePath NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_DocumentIsraelLaw (
    DocumentIsraelLawID NVARCHAR(MAX),
    IsraelLawID NVARCHAR(MAX),
    GroupTypeID NVARCHAR(MAX),
    GroupTypeDesc NVARCHAR(MAX),
    ApplicationID NVARCHAR(MAX),
    ApplicationDesc NVARCHAR(MAX),
    FilePath NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_DocumentLaw (
    DocumentLawID INT,
    LawID INT,
    GroupTypeID INT,
    GroupTypeDesc NVARCHAR(MAX),
    ApplicationID INT,
    ApplicationDesc NVARCHAR(MAX),
    FilePath NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_DocumentPlenumSession (
    DocumentPlenumSessionID INT,
    PlenumSessionID INT,
    GroupTypeID INT,
    GroupTypeDesc NVARCHAR(MAX),
    ApplicationID INT,
    ApplicationDesc NVARCHAR(MAX),
    FilePath NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_DocumentQuery (
    DocumentQueryID INT,
    QueryID INT,
    GroupTypeID INT,
    GroupTypeDesc NVARCHAR(MAX),
    ApplicationID INT,
    ApplicationDesc NVARCHAR(MAX),
    FilePath NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_Faction (
    FactionID INT,
    Name NVARCHAR(MAX),
    KnessetNum INT,
    StartDate NVARCHAR(MAX),
    FinishDate NVARCHAR(MAX),
    IsCurrent INT,
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_GovMinistry (
    GovMinistryID INT,
    Name NVARCHAR(MAX),
    IsActive INT,
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_IsraelLaw (
    IsraelLawID INT,
    KnessetNum FLOAT,
    Name NVARCHAR(MAX),
    IsBasicLaw FLOAT,
    IsFavoriteLaw FLOAT,
    PublicationDate NVARCHAR(MAX),
    LatestPublicationDate NVARCHAR(MAX),
    IsBudgetLaw FLOAT,
    LawValidityID INT,
    LawValidityDesc NVARCHAR(MAX),
    ValidityStartDate NVARCHAR(MAX),
    ValidityStartDateNotes NVARCHAR(MAX),
    ValidityFinishDate NVARCHAR(MAX),
    ValidityFinishDateNotes NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_IsraelLawBinding (
    IsraelLawBinding INT,
    IsraelLawID INT,
    IsraelLawReplacedID INT,
    LawID INT,
    LawTypeID INT,
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_IsraelLawClassificiation (
    LawClassificiationID INT,
    IsraelLawID INT,
    ClassificiationID INT,
    ClassificiationDesc NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_IsraelLawMinistry (
    LawMinistryID INT,
    IsraelLawID INT,
    GovMinistryID INT,
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_IsraelLawName (
    IsraelLawNameID INT,
    IsraelLawID INT,
    LawID INT,
    LawTypeID FLOAT,
    Name NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_ItemType (
    ItemTypeID INT,
    Desc NVARCHAR(MAX),
    TableName NVARCHAR(MAX)
);

CREATE TABLE KNS_JointCommittee (
    JointCommitteeID INT,
    CommitteeID INT,
    ParticipantCommitteeID INT,
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_KnessetDates (
    KnessetDateID INT,
    KnessetNum INT,
    Name NVARCHAR(MAX),
    Assembly INT,
    Plenum INT,
    PlenumStart NVARCHAR(MAX),
    PlenumFinish NVARCHAR(MAX),
    IsCurrent INT,
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_Law (
    LawID INT,
    TypeID INT,
    TypeDesc NVARCHAR(MAX),
    SubTypeID INT,
    SubTypeDesc NVARCHAR(MAX),
    KnessetNum FLOAT,
    Name NVARCHAR(MAX),
    PublicationDate NVARCHAR(MAX),
    PublicationSeriesID INT,
    PublicationSeriesDesc NVARCHAR(MAX),
    MagazineNumber NVARCHAR(MAX),
    PageNumber NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_LawBinding (
    LawBindingID INT,
    LawID INT,
    IsraelLawID INT,
    ParentLawID INT,
    LawTypeID INT,
    LawParentTypeID INT,
    BindingType INT,
    BindingTypeDesc NVARCHAR(MAX),
    PageNumber NVARCHAR(MAX),
    AmendmentType INT,
    AmendmentTypeDesc NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_MkSiteCode (
    MKSiteCode INT,
    KnsID INT,
    SiteId INT
);

CREATE TABLE KNS_Person (
    PersonID INT,
    LastName NVARCHAR(MAX),
    FirstName NVARCHAR(MAX),
    GenderID INT,
    GenderDesc NVARCHAR(MAX),
    Email NVARCHAR(MAX),
    IsCurrent INT,
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_PersonToPosition (
    PersonToPositionID INT,
    PersonID INT,
    PositionID INT,
    KnessetNum FLOAT,
    StartDate NVARCHAR(MAX),
    FinishDate NVARCHAR(MAX),
    GovMinistryID FLOAT,
    GovMinistryName NVARCHAR(MAX),
    DutyDesc NVARCHAR(MAX),
    FactionID FLOAT,
    FactionName NVARCHAR(MAX),
    GovernmentNum FLOAT,
    CommitteeID FLOAT,
    CommitteeName NVARCHAR(MAX),
    IsCurrent INT,
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_PlenumSession (
    PlenumSessionID INT,
    Number FLOAT,
    KnessetNum INT,
    Name NVARCHAR(MAX),
    StartDate NVARCHAR(MAX),
    FinishDate NVARCHAR(MAX),
    IsSpecialMeeting FLOAT,
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_PlmSessionItem (
    plmPlenumSessionID INT,
    ItemID INT,
    PlenumSessionID INT,
    ItemTypeID INT,
    ItemTypeDesc NVARCHAR(MAX),
    Ordinal INT,
    Name NVARCHAR(MAX),
    StatusID FLOAT,
    IsDiscussion INT,
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_Position (
    PositionID INT,
    Description NVARCHAR(MAX),
    GenderID INT,
    GenderDesc NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_Query (
    QueryID INT,
    Number FLOAT,
    KnessetNum INT,
    Name NVARCHAR(MAX),
    TypeID INT,
    TypeDesc NVARCHAR(MAX),
    StatusID INT,
    PersonID INT,
    GovMinistryID INT,
    SubmitDate NVARCHAR(MAX),
    ReplyMinisterDate NVARCHAR(MAX),
    ReplyDatePlanned NVARCHAR(MAX),
    LastUpdatedDate NVARCHAR(MAX)
);

CREATE TABLE KNS_Status (
    StatusID INT,
    Desc NVARCHAR(MAX),
    TypeID INT,
    TypeDesc NVARCHAR(MAX),
    OrderTransition FLOAT,
    IsActive FLOAT,
    LastUpdatedDate NVARCHAR(MAX)
);

